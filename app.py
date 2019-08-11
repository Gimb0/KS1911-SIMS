#!/usr/bin/env python3.6

# PyQt5 text editor example
# https://gist.github.com/olivierkes/a5ed456fb4313d248042b3ff29f5e754

import sys
import h5py
import numpy
from PyQt5.QtWidgets import * #QApplication, QMainWindow, QAction, qApp, QFileDialog, QLabel
from PyQt5.QtGui import * #QIcon
from regex import *

class Specie():

    def __init__(self, t, massA, massF, d, wt):
        self.speciesType = t
        self.speciesMassAMU = massA
        self.speciesMassField = massF
        self.detector = d
        self.WT = wt

    def getSpecieInfo(self):
        str = "Type is: " + self.speciesType + "\n"
        str += "Species Mass (amu) is: " + self.speciesMassAMU + "\n"
        str += "Species Mass (field) is: " + self.speciesMassField + "\n"
        str += "Detector is: " + self.detector + "\n"
        str += "WT (s) is: " + self.WT + "\n\n"
        return str

class DataSample():

    def __init__(self):
        self.species = []

    def setSampleID(self, id):
        self.sampleID = id
    
    def getSampleID(self):
        return self.sampleID

    def setSampleDate(self, date):
        self.sampleDate = date

    def setSampleTime(self, time):
        self.sampleTime = time

    def setSampleAcqTime(self, acqTime):
        self.totAcquisitionTime = acqTime

    def addSpecies(self, sType, sMassAMU, sMassField, detector, WT):
        self.species.append(Specie(sType, sMassAMU, sMassField, detector, WT))

    def getClassVars(self):
        str = '# ---- Class Info ----\n'
        str += 'Sample ID is: ' + self.sampleID + '\n'
        str += 'Sample Date is: ' + self.sampleDate + '\n'
        str += 'Sample Time is: ' + self.sampleTime + '\n'
        str += 'Total Acquisition time (s): ' + self.totAcquisitionTime + '\n'
        return str

    def getSpecies(self):
        str = "# ---- Species Info ----\n"
        for s in self.species:
            str += s.getSpecieInfo()
        return str


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
        ds = DataSample
        # Extract metadata not actual data
        with open(filename[0], 'r') as f:
            dfString = f.read()
            # Find all sample ID values in data and store first one
            sampleIdRegex = search(r'Sample ID\t\t(\w*|\W*)', dfString)
            self.ds.setSampleID(sampleIdRegex.group(1))

            analysisDateRegex = search(r'Analysis date\t\t(\d{2}\/\d{2}\/\d{4})', dfString)
            self.ds.setSampleDate(analysisDateRegex.group(1))

            analysisTimeRegex = search(r'Analysis time\t\t(\d{2}:\d{2})', dfString)
            self.ds.setSampleTime(analysisTimeRegex.group(1))

            acquisitionRegex = search(r'Total acquisition time \(s\)\t(\d+)', dfString)
            self.ds.setSampleAcqTime(acquisitionRegex.group(1))

        # Loop through file for data
        counter = -1
        data = ""
        with open(filename[0], 'r') as f:
            for line in f:
                if data == "" and counter == -1: # Look for data sections
                    if match(r'\*{3} MEASUREMENT CONDITIONS, \w+\.dp \*{3}:', line):
                        data = "MC"
                        counter = 3
                elif counter > 0:
                    counter -= 1
                    continue
                else:
                    if counter == 0:
                        if data == "MC":
                            while line != "\n":
                                s = line.replace(" ", "")
                                s = s.split('|')
                                s[-1] = s[-1].strip()
                                self.ds.addSpecies(s[0], s[1], s[2], s[3], s[4])
                                line = f.readline()
                            break

        print(self.ds.getClassVars())
        print(self.ds.getSpecies())
        self.text.setText(self.ds.getClassVars() + self.ds.getSpecies())

def main():
    app = QApplication(sys.argv)
    sims = Main()
    sims.show()
    app.exec_()

if __name__ == "__main__":
    sys.exit(main())