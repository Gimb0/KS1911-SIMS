#!/usr/bin/env python3

import sys
from PyQt5 import QtWidgets, uic
from io import BytesIO, StringIO, SEEK_SET
import pandas as pd;
from datetime import timedelta, time
from db_utils import dbUtils

class MainUI(QtWidgets.QMainWindow):
    def __init__(self):
        super(MainUI, self).__init__()
        uic.loadUi('MainUI.ui', self)
        
        self.isFileOpen = False

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

        # Filter Button
        filterButton = self.findChild(QtWidgets.QPushButton, 'filterButton')
        filterButton.clicked.connect(self.filterSamples)

        # Clear Filter Button
        clearButton = self.findChild(QtWidgets.QPushButton, 'clearButton')
        clearButton.clicked.connect(self.updateExtractInterface)

        # Extract Data Button
        extractDataButton = self.findChild(QtWidgets.QPushButton, 'extractDataButton')
        extractDataButton.clicked.connect(self.extractData)

        self.getUIComponents()

        # Database class
        self.dbConn = dbUtils()

        self.initializeInputInterface()
        self.updateExtractInterface()

        # Show App Window
        self.show()

    def extractSimsData(self, handle):
        databuf = StringIO()
        self.dataPoints = 0
        for _ in range(4):
            next(handle)
        for line in handle:
            if line.startswith('*** DATA END ***') or not line.strip():
                databuf.seek(SEEK_SET)
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
        # Input Tab
        # Sample ID
        self.inputSampleID = self.findChild(QtWidgets.QLineEdit, 'sampleIDText')
        # Date of Analysis
        self.analysisDateValue = self.findChild(QtWidgets.QLineEdit, 'sampleDate')
        # Acquisition Time
        self.acqTimeTime = self.findChild(QtWidgets.QLineEdit, 'sampleAcqTime')
        # Sample Species
        self.speciesListText = self.findChild(QtWidgets.QLineEdit, 'speciesListText')
        # Primary Ions
        self.pIonsText = self.findChild(QtWidgets.QLineEdit, 'samplePriIONText')
        # Primary Ions Energy
        self.pIonsEnergyValue = self.findChild(QtWidgets.QLineEdit, 'priIonEValue')
        # Number of data points
        self.dataPointsText = self.findChild(QtWidgets.QLineEdit, 'sampleDataPoints')
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
        self.sputtRate = self.findChild(QtWidgets.QDoubleSpinBox, 'inputSputtRate')
        # Additional Notes
        self.addNotes = self.findChild(QtWidgets.QTextEdit, 'addNotesText')

        # Display Tab
        # Sample ID
        self.displaySampleID = self.findChild(QtWidgets.QLineEdit, 'displaySampleID')
        # Annealing Temperature
        self.displayAnnTemp = self.findChild(QtWidgets.QLineEdit, 'displayAnnTemp')
        # Annealing Time
        self.displayAnnTime = self.findChild(QtWidgets.QLineEdit, 'displayAnnTime')
        # Analysis Date
        self.displayAnalysisDate = self.findChild(QtWidgets.QLineEdit, 'displayAnalDate')
        # Total Acquisition Time
        self.displayTotAcqTime = self.findChild(QtWidgets.QLineEdit, 'displayAcqTime')
        # Data Points
        self.displayDataPoints = self.findChild(QtWidgets.QLineEdit, 'displayDataPoints')
        # Species List
        self.displaySpecies = self.findChild(QtWidgets.QLineEdit, 'displaySpeciesList')
        # Primary Ion
        self.displayPriIon = self.findChild(QtWidgets.QLineEdit, 'displayPriIon')
        # Primary Ion Energy
        self.displayPriIonEnergy = self.findChild(QtWidgets.QLineEdit, 'displayPriIonE')
        # Gas Composition
        self.displayGasComp = self.findChild(QtWidgets.QLineEdit, 'displayGasComp')
        # Cooling Method
        self.displayCoolingMethod = self.findChild(QtWidgets.QLineEdit, 'displayCoolMethod')
        # Matrix Composition
        self.displayMatrixComp = self.findChild(QtWidgets.QLineEdit, 'displayMatrixComp')
        # Sputtering Rate
        self.displaySputtRate = self.findChild(QtWidgets.QLineEdit, 'displaySputtRate')
        # Additional Notes
        self.displayAddNotes = self.findChild(QtWidgets.QTextEdit, 'displayAddNotes')

        # Extract Tab
        # Samples List
        self.samplesList = self.findChild(QtWidgets.QListWidget, 'samplesList')
        # Filter Species List
        self.filterSpeciesList = self.findChild(QtWidgets.QListWidget, 'filterSpeciesList')
        # Filter Annealing Temperature List
        self.filterAnnTempsList = self.findChild(QtWidgets.QListWidget, 'filterAnnTempList')
        # Filter Cooling Method List
        self.filterCoolingMethodList = self.findChild(QtWidgets.QListWidget, 'filterCoolingList')
        # Filter Gas Composition List
        self.filterGasCompList = self.findChild(QtWidgets.QListWidget, 'filterGasCompList')
        # Filter Matrix Composition List
        self.filterMatrixCompList = self.findChild(QtWidgets.QListWidget, 'filterMatrixCompList')
        # Processing Normalization Species List
        self.normList = self.findChild(QtWidgets.QListWidget, 'outNormList')
        # Output Species List
        self.specieList = self.findChild(QtWidgets.QListWidget, 'outSpeciesList')

    def initializeInputInterface(self):
        # Fill lists with data from database
        # Gas Comp
        for gas in self.dbConn.getGasComposition():
            self.gasComp.addItem(gas[0])
        # Matrix Comp
        for matrix in self.dbConn.getMatrixComposition():
            self.matrixComp.addItem(matrix[0])
        # Cooling Method
        for method in self.dbConn.getCoolingMethod():
            self.coolingMethod.addItem(method[0])

    def updateExtractInterface(self):
        # Samples List
        self.samplesList.clicked.connect(self.sampleSelected)
        self.samplesList.clear()
        for sample in self.dbConn.getSamples():
                self.samplesList.addItem(sample[0])

        # Filter Species List
        self.filterSpeciesList.clear()
        for specie in self.dbConn.getSpecies():
            if specie[0] == "":
                pass
            self.filterSpeciesList.addItem(specie[0])

        # Filter Annealing Temps List
        self.filterAnnTempsList.clear()
        for temp in self.dbConn.getAnnealingTemps():
            if temp[0] == "":
                pass
            self.filterAnnTempsList.addItem(str(temp[0]))

        # Filter Cooling Method List
        self.filterCoolingMethodList.clear()
        for method in self.dbConn.getCoolingMethod():
            if method[0] == "":
                pass
            self.filterCoolingMethodList.addItem(method[0])
        
        # Filter Gas Composition List
        self.filterGasCompList.clear()
        for gas in self.dbConn.getGasComposition():
            if gas[0] == "":
                pass
            self.filterGasCompList.addItem(gas[0])

        # Filter Matrix Composition List
        self.filterMatrixCompList.clear()
        for matrix in self.dbConn.getMatrixComposition():
            if matrix[0] == "":
                pass
            self.filterMatrixCompList.addItem(matrix[0])

    def updateInputInterface(self):
        try:
            self.sampleIDText.setText(self.sampleID)
            self.analysisDateValue.setText(self.analysisDate)
            self.acqTimeTime.setText(self.acqTime)
            self.speciesListText.setText(self.speciesListString)
            self.pIonsText.setText(self.pIons)
            self.pIonsEnergyValue.setText(self.pIonsEnergy)
            self.dataPointsText.setText(str(self.dataPoints))
        except Exception as e:
            self.createPopupMessage('Error', e[0])
            return

    def updateDisplayInterface(self, sampleID):
        sampleData = self.dbConn.getSampleMetadata(sampleID)
        sampleSpecies = self.dbConn.getSampleSpecies(sampleID)

        # Display sample details on Sample Information tab
        self.displaySampleID.setText(sampleData[0])
        self.displayAnalysisDate.setText(sampleData[2])
        self.displayTotAcqTime.setText(sampleData[3])
        self.displayAnnTemp.setText(str(sampleData[4]))
        self.displayAnnTime.setText(str(sampleData[5]))
        self.displayGasComp.setText(sampleData[6])
        self.displayCoolingMethod.setText(sampleData[7])
        self.displayMatrixComp.setText(sampleData[8])
        self.displaySputtRate.setText(str(sampleData[9]))
        self.displayPriIon.setText(sampleData[10])
        self.displayPriIonEnergy.setText(str(sampleData[11]))
        self.displayAddNotes.setText(sampleData[12])
        self.displayDataPoints.setText(str(sampleData[13]))

        speciesList = ""
        for specie in sampleSpecies:
            speciesList += specie[0] + ", "
        
        self.displaySpecies.setText(speciesList[:-2])
    
    def sampleSelected(self):
        # Get Sample ID
        sampleID = self.samplesList.currentItem().text()
        
        self.updateDisplayInterface(sampleID)

        # Add sample species to list on extract tab        
        self.normList.clear()
        self.specieList.clear()
        for specie in self.dbConn.getSampleSpecies(sampleID):
            self.normList.addItem(specie[0])
            self.specieList.addItem(specie[0])

    def openDataFile(self):
        try:
            filename = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')
            dataFile = open(filename[0], 'rt')
            # Check if datafile is valid
            if not dataFile.readline().startswith('*** DATA FILES ***'):
                self.createPopupMessage('Error', 'Invalid Data File')
                return
            self.isFileOpen = True
        except FileNotFoundError:
            # A file was not chosen or it was wrongly selected so do nothing
            self.createPopupMessage("Error", "Please select an existing data file")
            return
        
        try:
            # Extract data from data file
            for line in dataFile:
                if line.startswith('Sample ID'):
                    self.sampleID = line.split()[-1]
                if line.startswith('Analysis date'):
                    self.analysisDate = line.split()[-1]
                if line.startswith('*** DATA START ***'):
                    simsdata = self.extractSimsData(dataFile)
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
            self.df = pd.read_csv(simsdata, header=None, delim_whitespace=True, skip_blank_lines=True)
            simsdata.close()
            self.df.columns = self.header
        
        except Exception as e:
            self.createPopupMessage('Error', 'Error extracting information from File: ' + e.args[0])

        finally:
            dataFile.close()

    # Save Data File and User Input to SQLite Database
    def saveInputData(self):
        msg = "Successfully saved data to database"
        try:
            # Do nothing if file has not been opened
            if self.isFileOpen is not True:
                return
            # Pass necessary data to insert functions
            self.dbConn.insertSampleData(self.sampleID, self.df.to_json(), self.analysisDate, self.acqTime, self.annTemp.value(), self.annTime.value(), self.gasComp.currentText(), self.coolingMethod.currentText(), self.matrixComp.currentText(), self.sputtRate.value(), self.pIons, self.pIonsEnergy, self.addNotes.toPlainText(), self.dataPoints)
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
            msg = e.args[0]
        finally:    
            self.createPopupMessage('Message', msg)
            
        self.updateExtractInterface()

    def filterSamples(self):
        # Get list of samples filtered by species
        speciesQuery = ""
        if len(self.filterSpeciesList.selectedItems()) > 0:
            for specie in self.filterSpeciesList.selectedItems():
                if specie.text() == "":
                    next
                speciesQuery += "specie = \"" + specie.text() + "\" OR "
        samplesList1 = self.dbConn.getSamplesWithSpecies(speciesQuery[:-4])

        metadataQuery = ""

        # Add Annealing Temperature filters to query
        tempList = self.filterAnnTempsList.selectedItems()
        if len(tempList) > 0:
            metadataQuery += "("
            for temp in tempList:
                if temp.text() == "0.0":
                    next
                metadataQuery += "annealingTemp = " + temp.text() + " OR "
            metadataQuery = metadataQuery[:-4] + ") AND "
        # Add Cooling Method filters to query
        methodList = self.filterCoolingMethodList.selectedItems()
        if len(methodList) > 0:
            metadataQuery += "("
            for method in methodList:
                if method.text() == "":
                    next
                metadataQuery += "coolingMethod = \"" + method.text() + "\" OR "
            metadataQuery = metadataQuery[:-4] + ") AND "
        gasList = self.filterGasCompList.selectedItems()
        # Add Gas Composition filters to query
        if len(gasList) > 0:
            metadataQuery += "("
            for gas in gasList:
                if gas.text() == "":
                    next
                metadataQuery += "gasComposition = \"" + gas.text() + "\" OR "
            metadataQuery = metadataQuery[:-4] + ") AND "
        matrixList = self.filterMatrixCompList.selectedItems()
        # Add Matrix Composition filters to query
        if len(matrixList) > 0:
            metadataQuery += "("
            for matrix in matrixList:
                if matrix.text() == "":
                    next
                metadataQuery += "matrixComposition = \"" + matrix.text() + "\" OR "
            metadataQuery = metadataQuery[:-4] + ")"
        else:
            metadataQuery = metadataQuery[:-5]
        
        samplesList2 = self.dbConn.getSamplesWithMetadata(metadataQuery)

        # Combine Sample lists and add to GUI list
        if speciesQuery == "" and metadataQuery == "":
            return
        elif speciesQuery == "":
            self.samplesList.clear()
            for sample in samplesList2:
                self.samplesList.addItem(sample[0])
        elif metadataQuery == "":
            self.samplesList.clear()
            for sample in samplesList1:
                self.samplesList.addItem(sample[0])
        else:
            self.samplesList.clear()
            for sample in set(samplesList1) and set(samplesList2):
                self.samplesList.addItem(sample[0])

    def createPopupMessage(self, title="Title", msg="Message"):
        QtWidgets.QMessageBox.about(self, title, msg)

    def extractData(self):
        # Check if necessary items have been selected
        sample = self.samplesList.selectedItems()
        normSpecies = self.normList.selectedItems()
        outputSpecies = self.specieList.selectedItems()
        if len(sample) == 0:
            self.createPopupMessage("Error", "Select a sample to extract data from")
            return
        elif len(normSpecies) == 0 or len(self.normList.selectedItems()) > 2:
            self.createPopupMessage("Error", "Select 1 or 2 normalisation species")
            return
        elif len(outputSpecies) == 0:
            self.createPopupMessage("Error", "Select species to output")
            return

        sampleID = sample[0].text()
        simsData = pd.read_json(self.dbConn.getSimsData(sampleID)[0])

        # Get all columns for time
        time = simsData.columns[simsData.columns.str.startswith('time')]

        # Calculate and store depth for each row
        depthDF = pd.DataFrame({'Depth (nm)':simsData[time].mean(axis=1)})
        depthDF['Depth (nm)'] = depthDF['Depth (nm)'] * float(self.displaySputtRate.text())

        # Calculate normalization factor
        # Create dataframe with 1 column 
        
        # 1 species selected
        if len(normSpecies) == 1:
            normDF = pd.DataFrame({'Normalization Factor':simsData['count-'+normSpecies[0].text()]})
        # 2 species selected
        elif len(normSpecies) == 2:
            normDF = pd.DataFrame({'Normalization Factor':simsData['count-'+normSpecies[0].text()]*simsData['count-'+normSpecies[1].text()]})

        # Get list of every species count
        speciesList1 = []
        speciesList2 = []
        fileNameStr = ""

        # Every species in sample  
        species = simsData.columns[simsData.columns.str.startswith('count')]
        for s in species:
            speciesList1.append(s)
        # Every species selected  
        for specie in outputSpecies:
            speciesList2.append('count-'+specie.text())
            fileNameStr += specie.text() + '_'
        
        # List of every selected species in sample
        speciesList = list(set(speciesList1) & set(speciesList2))
        
        speciesDF = simsData[speciesList]

        for specie in speciesList:
            speciesDF[specie] = speciesDF[specie] / normDF['Normalization Factor']

        # Merge depth dataframe and species dataframe
        processedDF = pd.merge(depthDF, speciesDF, left_index=True, right_index=True)

        # Allow user to select where to save file
        try:
            fName = sampleID + '_' + fileNameStr + '.csv'
            filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', fName)
            processedDF.to_csv(filename[0])
        except:
            processedDF.to_csv(fName)
            self.createPopupMessage('Error', 'Saved File elsewhere' + fName)


    def closeApp(self):
        self.dbConn.dbClose()
        sys.exit(0)

app = QtWidgets.QApplication(sys.argv)
window = MainUI()
app.exec_()
app.aboutToQuit(window.closeApp())