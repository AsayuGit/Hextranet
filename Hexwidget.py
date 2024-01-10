from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *
from overrides import override

from EditWidget import EditWidget
from OffsetArea import OffsetArea
from ByteIndexArea import ByteIndexArea

class Hexwidget(EditWidget):
    def __init__(self, dataStore):
        super().__init__(dataStore, 48, 3)
        
        # Custom Property
        self.editProgress = False

        # Widget Settings
        self.marginSize = QSize(50, 20)

        # Child Widgets
        self.lineNumberArea = OffsetArea(self)
        self.byteIndexArea = ByteIndexArea(self)

        # Event Connections
        self.blockCountChanged.connect(self.updateLineNumberWidth)
        self.verticalScrollBar().valueChanged.connect(self.lineNumberArea.scrollHandler)
        self.indexChanged.connect(self.clearProgress)

        # Final Setup
        self.updateLineNumberWidth()
        self.refreshWidgets()

    @override
    def applyInput(self, input, index):
        data = self.dataStore.getData()

        if self.editProgress:
            self.dataStore.setData(index, (data[index] & 0xF0) | (input & 0x0F))
            self.editProgress = False
        else:
            self.dataStore.setData(index, (input << 4) | (data[index] & 0xF))
            self.editProgress = True

    def clearProgress(self):
        self.editProgress = False
    
    @override
    def translateData(self, data: list):
        text = ""

        for b in data:
            text += f"{b:02X} "

        return text
    
    @override
    def translateInput(self, key: str):
        if key.isnumeric():
            return int(key)
        elif key.isalpha():
            value = ord(key.upper()[0]) - 0x41
            if value < 0 or value > 5: return None
            return value + 0xA
        else:
            return None

    # Maybe merge up
    @override
    def cursorPosChanged(self):
        linePos = self.textCursor().positionInBlock()
        if (linePos % self.itemSize) == (self.itemSize - 1):
            self.itemRight()
            self.updateCursor()

        return super().cursorPosChanged()

    @override
    def highlightText(self):
        lineSelection = QTextEdit.ExtraSelection()
        lineSelection.format.setBackground(Qt.gray)
        lineSelection.cursor = self.textCursor()
        lineSelection.format.setProperty(QTextFormat.FullWidthSelection, True)

        byteSelection = QTextEdit.ExtraSelection()
        byteSelection.format.setBackground(Qt.yellow)
        byteSelection.format.setForeground(Qt.red)
        byteSelection.cursor = self.textCursor()
        byteSelection.cursor.movePosition(QTextCursor.StartOfWord, QTextCursor.MoveAnchor)
        byteSelection.cursor.movePosition(QTextCursor.EndOfWord, QTextCursor.KeepAnchor)

        self.setExtraSelections([lineSelection, byteSelection])

    def updateLineNumberWidth(self):
        # Set the margins Size
        self.setViewportMargins(self.marginSize.width(), self.marginSize.height(), 0, 0)

    def refreshWidgets(self):
        self.lineNumberArea.update()