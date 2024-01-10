from typing import Optional
from PySide6.QtCore import *
import PySide6.QtCore
import PySide6.QtGui
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from overrides import override

class OffsetArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.hexwidget = parent
        self.move(0, self.hexwidget.marginSize.height())
        self.scrollOffset = 0

    # The widget recommanded size
    @override
    def sizeHint(self) -> QSize:
        return QSize(self.hexwidget.marginSize.width(), self.hexwidget.height() - self.hexwidget.marginSize.height())

    @override
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.fillRect(event.rect(), Qt.lightGray)
        painter.setPen(Qt.black)

        block = self.hexwidget.firstVisibleBlock()

        # for each line
        while block.isValid() and block.isVisible():
            blockNumber = block.blockNumber()

            # Figure out line boundaries
            top = round(self.hexwidget.blockBoundingGeometry(block).translated(self.hexwidget.contentOffset()).top()) + 1
            bottom = top + round(self.hexwidget.blockBoundingRect(block).height())

            # Draw the line offset
            painter.drawText(0, top, self.hexwidget.marginSize.width(), self.fontMetrics().height(), Qt.AlignRight, f"{blockNumber * 16:#04x}")

            # get next line
            block = block.next()

    def scrollHandler(self):
        self.scroll(0, self.hexwidget.verticalScrollBar().value())
