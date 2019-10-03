import sys
from PyQt5 import QtWidgets, uic
from io import StringIO
import pandas as pd;
from datetime import timedelta, time
from db_utils import dbUtils
from DialogUI import MsgDialog

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        # Class Variables
        self.isFileOpen = False


        super(MainUI, self).__init__()
        uic.loadUi('../uiFiles/MainUI.ui', self)

        # Add Actions to buttons and menus

        # Open Menu Button
        openFile = self.findChild(QtWidgets.QAction, 'actionOpenFile')
        openFile.triggered.connect(self.openDataFile)
        
        # Exit Menu Button
        exitApp = self.findChild(QtWidgets.QAction, 'actionExit')
        exitApp.triggered.connect(self.closeApp)

        # Save Button
        saveDataButton = self.findChild(QtWidgets.QPushButton, 'saveDataButton')
        saveDataButton.clicked.connect(self.saveInputData)

        # Open Button
        openFileButton = self.findChild(QtWidgets.QPushButton, 'openDFButton')
        openFileButton.clicked.connect(self.openDataFile)

        # Extract Data Button
        extractDataButton = self.findChild(QtWidgets.QPushButton, 'extractDataButton')
        extractDataButton.clicked.connect(self.extractData)

        # Database class
        self.dbConn = dbUtils()

        self.initializeExtractInterface()

        # Show App Window
        self.show()

    def extractSimsData(self, handle):
        databuf = StringIO()
        self.dataPoints = 0
        for _ in range(4):
            next(handle)
        for line in handle:
            if line.startswith('*** DATA END ***') or not line.strip():
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
            else:
                return names

    def getUIComponents(self):
        # Annealing Temperature
        self.annTemp = self.findChild(QtWidgets.QDoubleSpinBox, 'inputAnnTemp')

        # Annealing Time
        self.annTime = self.findChild(QtWidgets.QDoubleSpinBox, 'inputAnnTime')

        # Gas Composition
        self.gasComp = self.findChild(QtWidgets.QComboBox, 'inputGasComposition')

        # Cooling Method
        self.coolingMethod = self.findChild(QtWidgets.QComboBox, 'inputCoolingMethod')

        # Matrix Composition
        self.matrixComp = self.findChild(QtWidgets.QComboBox, 'matrixCompComboBox')

        # Sputtering Rate
        self.sputtRate = self.findChild(QtWidgets.QDoubleSpinBox, 'sputtRateValue')

        # Additional Notes
        self.addNotes = self.findChild(QtWidgets.QTextEdit, 'addNotesText')

    def updateInputInterface(self):
        # try:
        self.sampleIDText = self.findChild(QtWidgets.QLineEdit, 'sampleIDText')
        self.sampleIDText.setText(self.sampleID)

        self.sampleDateDate = self.findChild(QtWidgets.QLineEdit, 'sampleDateDate')
        self.sampleDateDate.setText(self.analysisDate)

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

    def initializeExtractInterface(self):
        # Samples List
        self.samplesList = self.findChild(QtWidgets.QListWidget, 'samplesList')
        self.samplesList.clicked.connect(self.sampleSelected)
        self.samplesList.clear()
        for sample in self.dbConn.getSamples():
                self.samplesList.addItem(sample[0])

        # Filter Species List
        self.filterSpeciesList = self.findChild(QtWidgets.QListWidget, 'filterSpeciesList')
        self.filterSpeciesList.clear()
        for specie in self.dbConn.getSpecies():
            if specie[0] == "":
                pass
            self.filterSpeciesList.addItem(specie[0])

        # Filter Annealing Temps List
        self.filterAnnTempsList = self.findChild(QtWidgets.QListWidget, 'filterAnnTempList')
        self.filterAnnTempsList.clear()
        for temp in self.dbConn.getAnnealingTemps():
            if temp[0] == "":
                pass
            self.filterAnnTempsList.addItem(str(temp[0]))

        # Filter Cooling Method List
        self.filterCoolingMethodList = self.findChild(QtWidgets.QListWidget, 'filterCoolingList')
        self.filterCoolingMethodList.clear()
        for method in self.dbConn.getCoolingMethod():
            if method[0] == "":
                pass
            self.filterCoolingMethodList.addItem(method[0])
        
        # Filter Gas Composition List
        self.filterGasCompList = self.findChild(QtWidgets.QListWidget, 'filterGasCompList')
        self.filterGasCompList.clear()
        for gas in self.dbConn.getGasComposition():
            if gas[0] == "":
                pass
            self.filterGasCompList.addItem(gas[0])

        # Filter Matrix Composition List
        self.filterMatrixCompList = self.findChild(QtWidgets.QListWidget, 'filterMatrixCompList')
        self.filterMatrixCompList.clear()
        for matrix in self.dbConn.getMatrixComposition():
            if matrix[0] == "":
                pass
            self.filterMatrixCompList.addItem(matrix[0]) 
    
    def sampleSelected(self):
        sampleID = self.samplesList.currentItem().text()
        annTime = self.findChild(QtWidgets.QDoubleSpinBox, 'extractAnnTimeValue')
        annTime.setValue(self.dbConn.getAnnealingTime(sampleID)[0])

        sputtRate = self.findChild(QtWidgets.QDoubleSpinBox, 'extractSputtRateValue')
        sputtRate.setValue(self.dbConn.getSputteringRate(sampleID)[0])

        self.normList = self.findChild(QtWidgets.QListWidget, 'outNormList')
        self.normList.clear()
        self.specieList = self.findChild(QtWidgets.QListWidget, 'outSpeciesList')
        self.specieList.clear()
        for specie in self.dbConn.getSampleSpecies(sampleID):
            self.normList.addItem(specie[0])
            self.specieList.addItem(specie[0])

    def openDataFile(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
            with open(filename[0], 'rt') as dataFile:
                # Check if datafile is valid
                if not dataFile.readline().startswith('*** DATA FILES ***'):
                    return
                self.isFileOpen = True
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
                        
            self.updateInputInterface()
            
            # Create pandas data frame
            self.df = pd.read_csv(self.simsdata, header=None, delim_whitespace=True, skip_blank_lines=True)
            self.simsdata.close()
            self.df.columns = self.header

        except FileNotFoundError:
            # A file was not chosen or it was wrongly selected so do nothing
            pass

    # Save Data File and User Input to SQLite Database
    def saveInputData(self):
        msg = "Successfully saved data to database"
        try:
        # Do nothing if file has not been opened
            if self.isFileOpen is not True:
                return
            
            self.getUIComponents()
            # self.inputValidation() # Waiting on Shane
            
            # Pass necessary data to insert functions
            self.dbConn.insertSampleData(self.sampleID, self.df)
            self.dbConn.insertSampleMetadata(self.sampleID, self.annTemp.value(), self.annTime.value(), self.gasComp.currentText(), self.coolingMethod.currentText(), self.matrixComp.currentText(), self.sputtRate.value(), self.addNotes.toPlainText(), self.dataPoints)
            self.dbConn.insertAnnealingTemp(self.annTemp.value())
            self.dbConn.insertCoolingMethod(self.coolingMethod.currentText())
            self.dbConn.insertGasComp(self.gasComp.currentText())
            self.dbConn.insertMatrixComp(self.matrixComp.currentText())

            species = self.speciesListString.split()
            for specie in species:
                specie = specie.strip(',')
                self.dbConn.insertSpecies(specie)
                self.dbConn.insertIntSpecies(self.sampleID, specie)

            # Commit changes to database
            self.dbConn.dbCommit()
        
        except Exception as e:
            msg = e
        finally:    
            self.createPopupMessage(msg)
        self.initializeExtractInterface()

    def createPopupMessage(self, title="Title", msg="Message"):
        QtWidgets.QMessageBox.about(self, title, msg)

    def extractData(self):
        # Check if necessary items have been selected
        if len(self.samplesList.selectedItems()) == 0:
            self.createPopupMessage("Error", "Select a sample to extract data from")
            return
        elif len(self.normList.selectedItems()) == 0 or len(self.normList.selectedItems()) > 2:
            self.createPopupMessage("Error", "Select 1 or 2 normalisation species")
            return
        elif len(self.specieList.selectedItems()) == 0:
            self.createPopupMessage("Error", "Select species to output")
            return

        # Get data to extract
        species = []
        sampleID = self.samplesList.currentItem().text()
        simsData = StringIO(self.dbConn.getSimsData(sampleID)[0])
        simsDF = pd.read_csv(simsData)
        for specie in self.specieList.selectedItems():
            species.append(specie.text())

        # Extract selected species
        numOfColumns = len(simsDF.columns[0].split())
        for index, row in simsDF.iterrows():
            print(row)
            return

    def closeApp(self):
        self.dbConn.dbClose()
        sys.exit(0)