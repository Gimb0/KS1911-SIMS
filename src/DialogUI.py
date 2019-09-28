from PyQt5 import QtWidgets, uic

class MsgDialog(QtWidgets.QDialog):
    def __init__(self):
        super(MsgDialog, self).__init__()
        uic.loadUi('../uiFiles/MsgUI.ui', self)

        closeButton = self.findChild(QtWidgets.QPushButton, 'closeButton')
        closeButton.clicked.connect(self.closeDialog)
        
        self.show()

    def closeDialog(self):
        self.close()

    def setMsg(self, msg):
        msgText = self.findChild(QtWidgets.QTextBrowser, 'msgTextBrowser')
        msgText.setText(msg)
