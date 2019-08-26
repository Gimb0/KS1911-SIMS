#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, uic

class HelpUI(QtWidgets.QMessageBox):
    def __init__(self):
        super(HelpUI, self).__init__()
        uic.loadUi('guiFiles/HelpUI.ui', self)

        self.show()

class MainUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi('guiFiles/MainUI.ui', self)

        # Add Action for Open File in Menu Bar
        self.openFile = self.findChild(QtWidgets.QAction, 'actionOpenFile')
        self.openFile.triggered.connect(self.openDataFile)
        
        # Get Pointer to Data Browser Component
        self.rawDataBrowser = self.findChild(QtWidgets.QTextBrowser, 'rawDataBrowser')

        # Get Pointer to Help Button
        self.helpButton = self.findChild(QtWidgets.QPushButton, 'extractHelpButton')
        self.helpButton.clicked.connect(self.showHelp)
        
        self.show()

    def openDataFile(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
            with open(filename[0], 'r') as dataFile:
                self.rawDataBrowser.setText(dataFile.read())
        except FileNotFoundError:
            # A file was not chosen so do nothing
            pass

    def showHelp(self):
        help = HelpUI()
        help.exec_()

app = QtWidgets.QApplication(sys.argv)
window = MainUI()
app.exec_()
