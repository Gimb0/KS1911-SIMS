#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, uic

class MainUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi('programFiles/MainUI.ui', self)

        # Add Action for Open File in Menu Bar
        self.openFile = self.findChild(QtWidgets.QAction, 'actionOpenFile')
        self.openFile.triggered.connect(self.openDataFile)

        self.show()


    def openDataFile(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
            # with open(filename[0], 'r') as dataFile:
        except FileNotFoundError:
            # A file was not chosen so do nothing
            pass

app = QtWidgets.QApplication(sys.argv)
window = MainUI()
app.exec_()
