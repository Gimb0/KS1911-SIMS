#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, uic

class Ui(QtWidgets.QMainWindow):

    def __init__(self):
        super(Ui, self).__init__()
        uic.loadUi('guiFiles/Test1.ui', self)

        # Add Action for Open File in Menu Bar
        self.openFile = self.findChild(QtWidgets.QAction, 'actionOpenFile')
        self.openFile.triggered.connect(self.openDataFile)
        
        # Get Pointer to Data Browser Component
        self.rawDataBrowser = self.findChild(QtWidgets.QTextBrowser, 'rawDataBrowser')
        
        self.show()

    def openDataFile(self):
        filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
        with open(filename[0], 'r') as dataFile:
            self.rawDataBrowser.setText(dataFile.read())

app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec_()
