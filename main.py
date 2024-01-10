import sys
from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from FileHexEditor import FileHexEditor
from NetworkHexEditor import NetworkHexEditor

import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Application Settings
        self.setMinimumSize(750, 1200)

        # Widgets
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Menu Bar
        self.menuBar = QMenuBar()
        self.fileMenu = self.menuBar.addMenu("&File")

        # Tabs
        self.tabs = QTabWidget()
        self.tabs.setTabsClosable(True)

        # Dialogs
        self.openFileDialog = QFileDialog(self)
        self.openFileDialog.setFileMode(QFileDialog.ExistingFile)
        self.openFileDialog.setWindowTitle("Open File...")
        self.openFileDialog.fileSelected.connect(self.doFilePicked)

        self.openUrlDialog = QInputDialog(self)
        self.openUrlDialog.setWindowTitle("Open remote file...")
        self.openUrlDialog.setInputMode(QInputDialog.TextInput)
        self.openUrlDialog.setLabelText("URL:")
        self.openUrlDialog.setTextValue("http://")
        self.openUrlDialog.resize(500, 100)
        self.openUrlDialog.textValueSelected.connect(self.doUrlPicked)

        # Menu Bar Actions
        self.openAction = QAction("&Open File", self)
        self.openAction.setToolTip("Open a file from disk")
        self.openAction.triggered.connect(self.doOpenFileAction)

        self.openUrlAction = QAction("Open &Remote File", self)
        self.openUrlAction.setToolTip("Open a file from an URL")
        self.openUrlAction.triggered.connect(self.doOpenUrlAction)

        self.saveAction = QAction("&Save File", self)
        self.saveAction.setToolTip("Save file to disk")
        self.saveAction.triggered.connect(self.doSaveFileAction)

        self.saveAsAction = QAction("&Save File As", self)
        self.saveAsAction.setToolTip("Save file to disk at path")
        self.saveAsAction.triggered.connect(self.doSaveAsFileAction)

        self.exitAction = QAction("&Exit", self)
        self.exitAction.setToolTip("Exit the program")
        self.exitAction.triggered.connect(self.doExitAction)

        # Tabs actions
        self.tabs.tabCloseRequested.connect(self.doCloseTab)
        
        # Assign menu bar actions
        self.fileMenu.addAction(self.openAction)
        self.fileMenu.addAction(self.openUrlAction)
        self.fileMenu.addAction(self.saveAction)
        self.fileMenu.addAction(self.saveAsAction)
        self.fileMenu.addAction(self.exitAction)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.menuBar)
        layout.addWidget(self.tabs)

        central_widget.setLayout(layout)

    def doOpenFileAction(self):
        self.openFileDialog.open()

    def doOpenUrlAction(self):
        self.openUrlDialog.open()

    def doFilePicked(self, file: str):
        file = file.strip()
        self.tabs.addTab(FileHexEditor(file), os.path.basename(file))

    def doUrlPicked(self, url: str):
        url = url.strip()
        self.tabs.addTab(NetworkHexEditor(url), os.path.basename(url))

    def doSaveFileAction(self):
        widget = self.tabs.currentWidget()
        if widget is not None: widget.saveData()

    def doSaveAsFileAction(self):
        widget = self.tabs.currentWidget()
        if widget is not None: widget.saveDataAs()

    def doCloseTab(self, id: int):
        self.tabs.removeTab(id)

    def doExitAction(self):
        exit(0)

app = QApplication(sys.argv)
window = MainWindow()
window.setWindowTitle("Hexeditor")
window.show()
app.exec()
