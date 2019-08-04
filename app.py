#!/usr/bin/env python3.6

# PyQt5 text editor example
# https://gist.github.com/olivierkes/a5ed456fb4313d248042b3ff29f5e754

import sys
import h5py
import numpy
from PyQt5.QtWidgets import * #QApplication, QMainWindow, QAction, qApp, QFileDialog, QLabel
from PyQt5.QtGui import * #QIcon
from regex import match

class DataSample():
    sampleID = None
    sampleDate = None
    sampleTime = None

    def setSampleID(id):
        sampleID = id
    
    def getSampleID():
        return sampleID

    def setSampleDate(date):
        sampleDate = date

    def setSampleTime(time):
        sampleTime = time

class Main(QMainWindow):
    # ----- Variables -----
    ds = DataSample()


    def __init__(self):
        super().__init__()
        self.initUI()        

    def initUI(self):
        # ----- Windows Settings -----
        self.resize(400, 420)
        self.setWindowTitle('SIMS Data Extractor')


        # ----- Menubar -----
        menubar = self.menuBar()
        # menubar.setNativeMenuBar(False) # Add menubar to top of window for Mac OS
        fileMenu = menubar.addMenu('File')
        
        dlg = QFileDialog(self)
        openAction = QAction('Open File', self)
        openAction.triggered.connect(self.openDataFile)
        fileMenu.addAction(openAction)


        # ----- Display Text -----
        self.text = QTextEdit(self)
        self.setCentralWidget(self.text)
    
    def openDataFile(self):
        filename = QFileDialog.getOpenFileName(self, 'Open File')
        info = ""
        with open(filename[0], 'r') as f:
            for line in f:
                if match(r'^Sample ID', line): # Extract Sample ID
                    ID_line = line.split(' ')[1]
                    ID_line = ID_line.strip('ID')
                    ID_line = ID_line.strip()
                    self.ds.setSampleID(ID_line)
                    info += ID_line + "\n"
                elif match(r'^Analysis date', line): # Extract sample date
                    info += line
                elif match(r'^Analysis time', line): # Extract sample time
                    info += line
        self.text.setText(info)
        print(self.ds.getSampleID())

def main():
    app = QApplication(sys.argv)
    sims = Main()
    sims.show()
    app.exec_()

if __name__ == "__main__":
    sys.exit(main())
