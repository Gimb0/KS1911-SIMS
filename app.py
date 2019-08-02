#!/usr/bin/env python3

# PyQt5 text editor example
# https://gist.github.com/olivierkes/a5ed456fb4313d248042b3ff29f5e754

import sys
import h5py
import numpy
from PyQt5.QtWidgets import QApplication, QMainWindow, QAction, qApp, QFileDialog, QMessageBox
from PyQt5.QtGui import QIcon

class SIMS_Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        menubar = self.menuBar()
        # menubar.setNativeMenuBar(False) # Add menubar to top of window for Mac OS
        fileMenu = menubar.addMenu('File')
        
        self.resize(400, 420)
        self.setWindowTitle('SIMS Data Extractor')

        dlg = QFileDialog(self)
        openAction = QAction('Open File', self)
        openAction.triggered.connect(self.selectDataFile)
        fileMenu.addAction(openAction)
    
    def openDataFile(self, filename):
        with open(filename) as data_file:
            for line in data_file:
                print(line)            

    def selectDataFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')
        #openDataFile(self, filename)
        with open(filename) as dataFile:
            for lines in dataFile:
                msg = QLabel(lines, self)
                break

def main():
    app = QApplication(sys.argv)
    sims = SIMS_Window()
    sims.show()
    app.exec_()

if __name__ == "__main__":
    sys.exit(main())
