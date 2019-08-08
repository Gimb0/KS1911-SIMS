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

    def setSampleID(self, id):
        self.sampleID = id
    
    def getSampleID(self):
        return self.sampleID

    def setSampleDate(self, date):
        self.sampleDate = date

    def setSampleTime(self, time):
        self.sampleTime = time

    def printClassVars(self):
        print('# ---- Class Info ----')
        print('Sample ID is: {}'.format(self.sampleID))
        print('Sample Date is: {}'.format(self.sampleDate))
        print('Sample Time is: {}'.format(self.sampleTime))


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
                    IDLine = line.split(' ')[1]
                    IDLine = IDLine.strip('ID')
                    IDLine = IDLine.strip()
                    self.ds.setSampleID(IDLine)
                    info += IDLine + "\n"
                elif match(r'^Analysis date', line): # Extract sample date
                    dateLine = line.split(' ')[1]
                    dateLine = dateLine.strip('date')
                    dateLine = dateLine.strip()
                    self.ds.setSampleDate(dateLine)
                    info += dateLine + "\n"
                elif match(r'^Analysis time', line): # Extract sample time
                    timeLine = line.split(' ')[1]
                    timeLine = timeLine.strip('time')
                    timeLine = timeLine.strip()
                    self.ds.setSampleTime(timeLine)
                    info += timeLine + '\n'
                
        self.text.setText(info)
        self.ds.printClassVars()

def main():
    app = QApplication(sys.argv)
    sims = Main()
    sims.show()
    app.exec_()

if __name__ == "__main__":
    sys.exit(main())
