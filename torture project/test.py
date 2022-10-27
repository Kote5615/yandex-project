import sys
from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_ChatWindow(object):
    def setupUi(self, ChatWindow):
        ChatWindow.setObjectName("ChatWindow")
        ChatWindow.setEnabled(True)
        ChatWindow.resize(319, 480)
        self.centralwidget = QtWidgets.QWidget(ChatWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.background = QtWidgets.QLabel(self.centralwidget)
        self.background.setGeometry(QtCore.QRect(0, 0, 321, 480))
        self.background.setAutoFillBackground(False)
        self.background.setStyleSheet("image: url(:/newPrefix/чат с кнопкой.png);")
        self.background.setText("")
        self.background.setWordWrap(False)
        self.background.setIndent(1)
        self.background.setObjectName("background")
        self.input_msg = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.input_msg.setGeometry(QtCore.QRect(7, 414, 249, 54))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.input_msg.setFont(font)
        #        self.input_msg.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n""border: 2px green;")
        self.input_msg.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.input_msg.setCenterOnScroll(False)
        self.input_msg.setObjectName("input_msg")
        self.btn_send = QtWidgets.QPushButton(self.centralwidget)
        self.btn_send.setGeometry(QtCore.QRect(263, 416, 51, 51))
        self.btn_send.setMouseTracking(False)
        #        self.btn_send.setStyleSheet("image: url(:/newPrefix/кнопка отправить.png);\n""background-color: rgba(255, 255, 255, 0);")
        self.btn_send.setText("")
        self.btn_send.setObjectName("btn_send")
        self.plainTextEdit_2 = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit_2.setGeometry(QtCore.QRect(7, 15, 306, 390))
        font = QtGui.QFont()
        font.setPointSize(12)
        font.setBold(False)
        font.setItalic(False)
        font.setUnderline(False)
        font.setWeight(50)
        font.setStrikeOut(False)
        self.plainTextEdit_2.setFont(font)
        #        self.plainTextEdit_2.setStyleSheet("background-color: rgba(255, 255, 255, 0);\n""border: 2px green;")
        self.plainTextEdit_2.setReadOnly(True)
        self.plainTextEdit_2.setPlainText("")
        self.plainTextEdit_2.setOverwriteMode(False)
        self.plainTextEdit_2.setBackgroundVisible(False)
        self.plainTextEdit_2.setCenterOnScroll(False)
        self.plainTextEdit_2.setObjectName("plainTextEdit_2")
        ChatWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ChatWindow)
        QtCore.QMetaObject.connectSlotsByName(ChatWindow)

    def retranslateUi(self, ChatWindow):
        _translate = QtCore.QCoreApplication.translate
        ChatWindow.setWindowTitle(_translate("ChatWindow", "Чат"))


class ChatWindow(QtWidgets.QMainWindow, Ui_ChatWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.btn_send.clicked.connect(self.send_msg)

    def send_msg(self):
        text = self.input_msg.toPlainText()
        if text:
            self.plainTextEdit_2.appendPlainText(self.input_msg.toPlainText())
            self.input_msg.clear()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    w = ChatWindow()
    w.show()
    sys.exit(app.exec_())