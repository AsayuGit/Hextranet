from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from overrides import override
from abc import abstractclassmethod

import math

class EditWidget(QPlainTextEdit):
    indexChanged = Signal(int, int)
    
    def __init__(self, dataStore, lineLen: int, itemSize: int):
        super().__init__()

        self.dataStore = dataStore
        data = dataStore.getData()
        
        self.lineLen = lineLen
        self.itemSize = itemSize

        self.cursorRow = 0
        self.cursorCol = 0

        # Widget settings
        self.setFont(QFontDatabase.systemFont(QFontDatabase.FixedFont)) # Use a Fixed size font
        self.setViewportMargins(0, 20, 0, 0)
        self.setTextInteractionFlags(Qt.TextEditable)
        
        # Envent Connections
        self.cursorPositionChanged.connect(self.cursorPosChanged)

        self.refreshData()

    @abstractclassmethod
    def highlightText(self): pass

    @abstractclassmethod
    def translateData(self, data: list): pass

    @abstractclassmethod
    def translateInput(self, key: str): pass

    # At each keypress, put the corresponding ascii char in the data array
    # An move the cursor pos
    @override
    def keyPressEvent(self, e: QKeyEvent) -> None:
        if e.key() == Qt.Key.Key_Up:
            self.cursorUp()
            self.updateCursor()
        elif e.key() == Qt.Key.Key_Down:
            self.cursorDown()
            self.updateCursor()
        elif e.key() == Qt.Key.Key_Left:
            self.itemLeft()
            self.updateCursor()
        elif e.key() == Qt.Key.Key_Right:
            self.itemRight()
            self.updateCursor()
        else:
            input = self.translateInput(e.text())
            if input is not None:
                self.applyInput(input, self.getDataPos())
                self.cursorRight()
                self.updateCursor()
                self.refreshData()

    def applyInput(self, input, index):
        self.dataStore.setData(index, input)

    def itemRight(self):
        # Ensure we're at the start of the next item
        self.cursorCol = (math.floor(self.cursorCol / self.itemSize) * self.itemSize) + self.itemSize

        if self.cursorCol >= self.lineLen:
            self.cursorCol = 0
            self.cursorRow += 1

        self.indexChanged.emit(self.cursorCol, self.cursorRow)

    def itemLeft(self):
        if self.cursorRow > 0 and self.cursorCol <= 0:
            self.cursorCol = self.lineLen - 1
            self.cursorRow -= 1
        elif self.cursorCol > 0:
            self.cursorCol -= self.itemSize

        if self.cursorCol < 0:
            self.cursorCol = 0

        self.indexChanged.emit(self.cursorCol, self.cursorRow)

        # Ensure we're at the start of the previous item
        self.cursorCol = (math.floor(self.cursorCol / self.itemSize) * self.itemSize)

    def cursorRight(self):
        # Ensure we're at the start of the next item
        self.cursorCol += 1

        if self.cursorCol >= self.lineLen:
            self.cursorCol = 0
            self.cursorRow += 1
    
    def cursorLeft(self):
        if self.cursorRow > 0 and self.cursorCol <= 0:
            self.cursorCol = self.lineLen - 1
            self.cursorRow -= 1
        elif self.cursorCol > 0:
            self.cursorCol -= 1

        # Ensure we're at the start of the previous item
        self.cursorCol = (math.floor(self.cursorCol / self.itemSize) * self.itemSize)

    def cursorUp(self):
        if self.cursorRow > 0:
            self.cursorRow -= 1
            self.indexChanged.emit(self.cursorCol, self.cursorRow)

    def cursorDown(self):
        self.cursorRow += 1
        self.indexChanged.emit(self.cursorCol, self.cursorRow)

    def getCursorPos(self):
        return self.cursorRow * self.lineLen + self.cursorCol
    
    def setCursorPos(self, pos):
        pass

    def getDataPos(self):
        return math.floor(self.getCursorPos() / self.itemSize)
    
    def getCursorCoordinates(self):
        return (self.cursorRow, math.floor(self.cursorCol / self.itemSize))
    
    def setCursorCoordinates(self, row, col):
        self.cursorRow = row
        self.cursorCol = col * self.itemSize
        self.updateCursor()

    def toNextLine(self):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.NextBlock, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

        self.indexChanged.emit(self.cursorCol, self.cursorRow)

    def cursorPosChanged(self):
        linePos = self.textCursor().positionInBlock()
        if linePos >= self.lineLen:
            self.toNextLine()


        oldCursorRow = self.cursorRow
        oldCursorCol = self.cursorCol

        self.cursorRow = self.textCursor().blockNumber()
        self.cursorCol = self.textCursor().positionInBlock()

        if (oldCursorRow != self.cursorRow) or (math.floor(oldCursorCol / self.itemSize) != math.floor(self.cursorCol / self.itemSize)):
            self.indexChanged.emit(self.cursorCol, self.cursorRow)

        self.highlightText()

    def updateCursor(self):
        cursor = self.textCursor()
        #  + to take in account the \n in the widget text
        pos = self.getCursorPos() + self.cursorRow

        cursor.setPosition(pos, QTextCursor.MoveAnchor)
        self.setTextCursor(cursor)

    def refreshData(self):
        text = self.translateData(self.dataStore.getData())
        text = self.formatText(text)
        
        self.blockSignals(True)
        self.setPlainText(text)
        self.blockSignals(False)

        self.updateCursor()
        self.highlightText()

    def formatText(self, text):
        return "\n".join(text[i:i + self.lineLen] for i in range(0, len(text), self.lineLen))