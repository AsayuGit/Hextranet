# https://raw.githubusercontent.com/AsayuGit/FooCalcRPL/main/src/CalcServer.java
# https://raw.githubusercontent.com/ianare/exif-samples/master/jpg/Canon_40D.jpg

from Hexeditor import Hexeditor

from PySide6.QtCore import *
from PySide6.QtWidgets import *
from PySide6.QtGui import *
from PySide6.QtNetwork import *

from overrides import override

class NetworkHexEditor(Hexeditor):
    def __init__(self, url: str):
        super().__init__()

        self.fileURL = url

        # Load data
        self.networkManager = QNetworkAccessManager()
        self.networkManager.finished.connect(self.handleResponse)

        # Additional Widgets
        self.headerData = QTableWidget()
        self.headerData.setColumnCount(2)
        self.headerData.setHorizontalHeaderLabels(["Header", "Value"])
        self.headerData.setColumnWidth(0, 150)
        self.headerData.setColumnWidth(1, 300)

        self.requestInfo = QPlainTextEdit()
        self.requestInfo.setTextInteractionFlags(Qt.NoTextInteraction)

        self.miscTabs.addTab(self.headerData, "HTTP Header")
        self.miscTabs.addTab(self.requestInfo, "Request Info")

        self.sendRequest(url)


    def sendRequest(self, url: str):
        self.headerData.setRowCount(0)
        self.requestInfo.clear()
        request = QNetworkRequest(QUrl(url))
        self.networkManager.get(request)

    def handleResponse(self, reply):
        if reply.error() == QNetworkReply.NoError:
            statusCode = reply.attribute(QNetworkRequest.HttpStatusCodeAttribute)
            self.requestInfo.appendPlainText(f"HTTP Status Code: {statusCode}")

            headers = reply.rawHeaderList()
            for header in headers:
                headerCell = QTableWidgetItem(header.data().decode("utf-8"))
                valueCell = QTableWidgetItem(reply.rawHeader(header).data().decode("utf-8"))

                self.headerData.insertRow(self.headerData.rowCount())
                self.headerData.setItem(self.headerData.rowCount() - 1, 0, headerCell)
                self.headerData.setItem(self.headerData.rowCount() - 1, 1, valueCell)

            content = reply.readAll().data()
            self.setEditorData(content)

        else:
            self.requestInfo.appendPlainText("Error: " + reply.errorString())

    @override
    def saveData(self):
        super().saveDataAs()