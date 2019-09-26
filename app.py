#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, uic
import io
import pandas as pd;
from datetime import timedelta, time
from db_utils import dbUtils


class MainUI(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi('programFiles/MainUI.ui', self)

        # Add Action for Open File in Menu Bar
        self.openFile = self.findChild(QtWidgets.QAction, 'actionOpenFile')
        self.openFile.triggered.connect(self.openDataFile)

        self.dbConn = dbUtils()

        self.show()

    def extractSimsData(self, handle):
        databuf = io.StringIO()
        self.dataPoints = 0
        for _ in range(4):
            next(handle)
        for line in handle:
            if line.startswith('*** DATA END ***') or not line.strip():
                databuf.seek(io.SEEK_SET)
                return databuf
            databuf.write(line)
            self.dataPoints += 1
    
    def extractSpeciesList(self, handle):
        names = []

        for _ in range(3):
            next(handle)
        for line in handle:
            if line.rstrip():
                name = line.split()[0]
                names.append(name)
                # names.extend([f'time-{name}', f'count-{name}'])
            else:
                return names

    def updateInterface(self):
        # try:
        self.sampleIDText = self.findChild(QtWidgets.QLineEdit, 'sampleIDText')
        self.sampleIDText.setText(self.sampleID)

        self.sampleDateDate = self.findChild(QtWidgets.QLineEdit, 'sampleDateDate')
        self.sampleDateDate.setText(self.analysisDate)
        # self.sampleDateDate = self.findChild(QtWidgets.QDateEdit, 'sampleDateDate')
        # self.sampleDateDate.setDate(self.analysisDate)
        
        self.acqTimeTime = self.findChild(QtWidgets.QLineEdit, 'sampleAcqTimeTime')
        self.acqTimeTime.setText(self.acqTime)

        self.speciesListText = self.findChild(QtWidgets.QLineEdit, 'speciesListText')
        self.speciesListText.setText(self.speciesListString)
        
        self.pIonsText = self.findChild(QtWidgets.QLineEdit, 'samplePriIONText')
        self.pIonsText.setText(self.pIons)

        self.pIonsEnergyValue = self.findChild(QtWidgets.QSpinBox, 'samplePriIONEValue')
        self.pIonsEnergyValue.setValue(int(self.pIonsEnergy))

        self.dataPointsText = self.findChild(QtWidgets.QLineEdit, 'sampleDataPointsText')
        self.dataPointsText.setText(str(self.dataPoints))
        # except:
        #     pass
    
    # def getUIComponents(self):


    def openDataFile(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
            with open(filename[0], 'rt') as dataFile:
                # Check if datafile is valid
                if not dataFile.readline().startswith('*** DATA FILES ***'):
                    return
                # Extract data from data file
                for line in dataFile:
                    if line.startswith('Sample ID'):
                        self.sampleID = line.split()[-1]
                    if line.startswith('Analysis date'):
                        self.analysisDate = line.split()[-1]
                    if line.startswith('*** DATA START ***'):
                        self.simsdata = self.extractSimsData(dataFile)
                    if line.startswith('Total acquisition time (s)'):
                        self.acqTime = int(line.split()[-1])
                        self.acqTime = str(timedelta(seconds=self.acqTime))
                    if line.startswith("*** MEASUREMENT CONDITIONS"):
                        speciesList = self.extractSpeciesList(dataFile)
                        self.header = []
                        self.speciesListString = ""
                        for specie in speciesList:
                            self.speciesListString += specie + ", "
                            self.header.extend([f'time-{specie}', f'count-{specie}'])
                        self.speciesListString = self.speciesListString[0:-2]
                    if line.startswith("Primary ions"):
                        self.pIons = line.split()[-1]
                    if line.startswith("Impact energy"):
                        self.pIonsEnergy = line.split()[-1]
                        
            self.updateInterface()
            
            # Create pandas data frame
            self.df = pd.read_csv(self.simsdata, header=None, delim_whitespace=True, skip_blank_lines=True)
            self.simsdata.close()
            self.df.columns = self.header
            print(self.df)

        except FileNotFoundError:
            # A file was not chosen or wrongly selected so do nothing
            pass

app = QtWidgets.QApplication(sys.argv)
window = MainUI()
app.exec_()
