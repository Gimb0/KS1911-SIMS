import sqlite3
import os

# Add option to open a database
DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'simsdatastore.sqlite3')

class dbUtils():
    def __init__(self):
        if not os.path.exists(DEFAULT_PATH) and not os.path.isfile(DEFAULT_PATH):
            self.createDB()
        else:
            self.con = self.dbConnect()
            self.cur = self.con.cursor()

    def dbConnect(self, dbPath=DEFAULT_PATH):
        return sqlite3.connect(dbPath)

    def dbClose(self):
        self.cur.close()
        self.con.close()

    def dbCommit(self):
        self.con.commit()

    # Create SQLite3 DB here
    def createDB(self):
        self.con = self.dbConnect()
        self.cur = self.con.cursor()
        
        # Create Sample Data Table
        sampleMDTable = """CREATE TABLE sampleData (
            sampleID TEXT PRIMARY KEY,
            simsData BLOB,
            acquisitionDate TEXT,
            totalAcquisitionTime TEXT,
            annealingTemp REAL,
            annealingTime REAL,
            gasComposition TEXT,
            coolingMethod TEXT,
            matrixComposition TEXT,
            sputteringRate REAL,
            primaryIon TEXT,
            primaryIonEnergy REAL,
            additionalNotes TEXT,
            dataPoints INTEGER
        ) """
        self.cur.execute(sampleMDTable)

        matrixCompTable = """CREATE TABLE matrixCompositions (
            matrix TEXT PRIMARY KEY
        )"""
        self.cur.execute(matrixCompTable)

        # Create Gas Composition Table
        gasCompTable = """CREATE TABLE gasCompositions (
            gas TEXT PRIMARY KEY
        )"""
        self.cur.execute(gasCompTable)

        # Create Cooling Method Table
        coolingMethodTable = """CREATE TABLE coolingMethod (
            method TEXT PRIMARY KEY
        )"""
        self.cur.execute(coolingMethodTable)

        # Create Annealing Temperature Table
        annealingTempTable = """CREATE TABLE annealingTemp (
            temperature REAL PRIMARY KEY
        )"""
        self.cur.execute(annealingTempTable)

        # Create Species Table
        speciesTable = """CREATE TABLE species (
            specie TEXT PRIMARY KEY
        )"""
        self.cur.execute(speciesTable)

        # Create intermediate species table
        intSpeciesTable = """CREATE TABLE intSpecies (
            sampleID TEXT,
            specie TEXT NOT NULL,
            FOREIGN KEY (specie) REFERENCES species(specie)
        )"""
        self.cur.execute(intSpeciesTable)
    
    # Insert to or Update the sampleData Table
    def insertSampleData(self, sampleID=None, sampleData=None, acquisitionDate=None, totalAcquistionTime=None, annealingTemp=None, annealingTime=None, gasComposition=None, coolingMethod=None,  matrixComposition=None, sputteringRate=None, primaryIon=None, primaryIonEnergy=None, additionalNotes=None, dataPoints=None):
        # Sample ID must not be None, everything else can be
        if sampleID == None:
            return

        # Check if row exists with current sampleID
        self.cur.execute("""SELECT sampleID FROM sampleData WHERE sampleID = ?""", (sampleID, ))
        data = self.cur.fetchone()
        # Insert row if doesn't exist
        if data == None:
            self.cur.execute("INSERT INTO sampleData (sampleID, simsData, acquisitionDate, totalAcquisitionTime, annealingTemp, annealingTime, gasComposition, coolingMethod, matrixComposition, sputteringRate, primaryIon, primaryIonEnergy, additionalNotes, dataPoints  ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (sampleID, sampleData, acquisitionDate, totalAcquistionTime, annealingTemp, annealingTime, gasComposition, coolingMethod, matrixComposition, sputteringRate, primaryIon, primaryIonEnergy, additionalNotes, dataPoints))
        # Update row if does exist
        else:
            self.cur.execute("""UPDATE sampleData SET annealingTemp = ?, annealingTime = ?, gasComposition = ?, coolingMethod = ?, matrixComposition = ?, sputteringRate = ?, additionalNotes = ? WHERE sampleID = ?""", (annealingTemp, annealingTime, gasComposition, coolingMethod, matrixComposition, sputteringRate, additionalNotes, sampleID))
    
    def insertGasComp(self, gasComposition):
        if gasComposition == "":
            return
        self.cur.execute("""SELECT gas FROM gasCompositions WHERE gas = ?""", (gasComposition, ))
        data = self.cur.fetchone()
        if data is None:
            self.cur.execute("INSERT INTO gasCompositions (gas) VALUES (?)", (gasComposition, ))

    def insertCoolingMethod(self, coolingMethod):
        if coolingMethod == "":
            return
        self.cur.execute("""SELECT method FROM coolingMethod WHERE method = ?""", (coolingMethod, ))
        data = self.cur.fetchone()
        if data is None:
            self.cur.execute("INSERT INTO coolingMethod (method) VALUES (?)", (coolingMethod, ))

    def insertAnnealingTemp(self, temperature):
        if temperature == 0.0:
            return
        self.cur.execute("""SELECT * FROM annealingTemp WHERE temperature = ?""", (temperature, ))
        data = self.cur.fetchone()
        if data is None:
            self.cur.execute("INSERT INTO annealingTemp (temperature) VALUES (?)", (temperature, ))

    def insertMatrixComp(self, matrix):
        if matrix == "":
            return
        self.cur.execute("""SELECT * FROM matrixCompositions WHERE matrix = ?""", (matrix, ))
        data = self.cur.fetchone()
        if data is None:
            self.cur.execute("""INSERT INTO matrixCompositions (matrix) VALUES (?)""", (matrix, ))

    def insertSpecies(self, specie):
        if specie == "":
            return
        self.cur.execute("""SELECT * FROM species WHERE specie = ?""", (specie, ))
        data = self.cur.fetchone()
        if data is None:
            self.cur.execute("INSERT INTO species (specie) VALUES (?)", (specie, )) 

    def insertIntSpecies(self, sampleID, specie):
        if sampleID is None or specie is None:
            return
        self.cur.execute("""SELECT * FROM intSpecies WHERE sampleID = ? AND specie = ?""", (sampleID, specie))
        data = self.cur.fetchone()
        if data is None:
            self.cur.execute("INSERT INTO intSpecies (sampleID, specie) VALUES (?,?)", (sampleID, specie))

    def getSamples(self):
        self.cur.execute("""SELECT sampleID FROM sampleData""")
        return self.cur.fetchall()

    def getSpecies(self):
        self.cur.execute("""SELECT specie from species""")
        return self.cur.fetchall()

    def getAnnealingTemps(self):
        self.cur.execute("""SELECT temperature FROM annealingTemp""")
        return self.cur.fetchall()

    def getAnnealingTime(self, sampleID):
        self.cur.execute("""SELECT annealingTime FROM sampleData WHERE sampleID = ?""", (sampleID, ))
        return self.cur.fetchone()

    def getCoolingMethod(self):
        self.cur.execute("""SELECT method FROM coolingMethod""")
        return self.cur.fetchall()

    def getGasComposition(self):
        self.cur.execute("""SELECT gas FROM gasCompositions""")
        return self.cur.fetchall()
    
    def getMatrixComposition(self):
        self.cur.execute("""SELECT matrix FROM matrixCompositions""")
        return self.cur.fetchall()

    def getSputteringRate(self, sampleID):
        self.cur.execute("""SELECT sputteringRate FROM sampleData WHERE sampleID = ?""", (sampleID, ))
        return self.cur.fetchone()

    def getSampleSpecies(self, sampleID):
        self.cur.execute("""SELECT specie FROM intSpecies WHERE sampleID = ?""", (sampleID, ))
        return self.cur.fetchall()

    def getSimsData(self, sampleID):
        self.cur.execute("""SELECT simsData FROM sampleData WHERE sampleID = ?""", (sampleID, ))
        return self.cur.fetchone()

    def getSampleMetadata(self, sampleID):
        self.cur.execute("""SELECT * FROM sampleData WHERE sampleID = ?""", (sampleID, ))
        return self.cur.fetchone()

    def getSamplesWithSpecies(self, filterQuery):
        if filterQuery == "":
            return []
        query = """SELECT DISTINCT sampleID FROM intSpecies WHERE """ + filterQuery
        self.cur.execute(query)
        return self.cur.fetchall()

    def getSamplesWithMetadata(self, filterQuery):
        if filterQuery == "":
            return []
        query = """SELECT sampleID FROM sampleData WHERE """ + filterQuery
        self.cur.execute(query)
        return self.cur.fetchall()