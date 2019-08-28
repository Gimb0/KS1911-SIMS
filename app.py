#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, uic

class HelpUI(QtWidgets.QDialog):
    def __init__(self):
        super(HelpUI, self).__init__()
        uic.loadUi('programFiles/HelpUI.ui', self)

        # Get pointer to text browser
        self.helpBrwoser = self.findChild(QtWidgets.QTextBrowser, 'helpBrowser')

    def extractHelp(self):
        # Display help message for extract options tab
        try:
            with open('programFiles/extractHelp.txt', 'r') as helpFile:
                self.helpBrwoser.setText(helpFile.read())
                self.show()
        except:
            self.close
    
    def aboutHelp(self):
        # Display help message for extract options tab
        try:
            with open('programFiles/aboutHelp.txt', 'r') as helpFile:
                self.helpBrwoser.setText(helpFile.read())
                self.show()
        except:
            self.close()

class MainUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi('programFiles/MainUI.ui', self)

        self.help = HelpUI()

        # Add Action for Open File in Menu Bar
        self.openFile = self.findChild(QtWidgets.QAction, 'actionOpenFile')
        self.openFile.triggered.connect(self.openDataFile)

        # Add action for extract options menubar option
        self.extractHelp = self.findChild(QtWidgets.QAction, 'actionExtractOptions')
        self.extractHelp.triggered.connect(self.extractOptionsHelp)

        # Add action for about menubar option
        self.aboutDialog = self.findChild(QtWidgets.QAction, 'actionAbout')
        self.aboutDialog.triggered.connect(self.aboutDialogBox)
        
        # Get Pointer to Data Browser Component
        self.rawDataBrowser = self.findChild(QtWidgets.QTextBrowser, 'rawDataBrowser')
        self.show()

    def openDataFile(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
            with open(filename[0], 'r') as dataFile:
                self.rawDataBrowser.setText(dataFile.read())
        except FileNotFoundError:
            # A file was not chosen so do nothing
            pass

    def extractOptionsHelp(self):
        self.help.extractHelp()
        self.help.exec_()

    def aboutDialogBox(self):
        self.help.aboutHelp()
        self.help.exec_()

app = QtWidgets.QApplication(sys.argv)
window = MainUI()
app.exec_()
