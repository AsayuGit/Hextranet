from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from overrides import override

class ByteIndexArea(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.hexwidget = parent
        self.move(self.hexwidget.marginSize.width(), 0)

    @override
    def sizeHint(self) -> QSize:
        return QSize(self.hexwidget.height() - self.hexwidget.marginSize.width(), self.hexwidget.marginSize.height())
    
    @override
    def paintEvent(self, event: QPaintEvent):
        painter = QPainter(self)
        painter.fillRect(event.rect(), Qt.lightGray)
        painter.setPen(Qt.black)
        
        painter.drawText(5, self.height() - self.fontMetrics().height(), self.width(), self.fontMetrics().height(), Qt.AlignLeft, (" ".join(f"{i:02x}" for i in range(0, 16))))