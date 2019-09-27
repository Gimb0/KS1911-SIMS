import sqlite3
import os

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

    # Create SQLite3 DB here
    def createDB(self):
        print("Creating database!!!")
        self.con = self.dbConnect()
        self.cur = self.con.cursor()

        # Create Sample Data Table
        sampleDataTable = """CREATE TABLE sampleData (
            sampleID TEXT PRIMARY KEY,
            simsData BLOB
        )"""
        self.cur.execute(sampleDataTable)
        
        # Create Sample Metadata Table
        sampleMDTable = """CREATE TABLE sampleMetadata (
            sampleID TEXT PRIMARY KEY,
            sputteringRate REAL,
            annealingTime REAL,
            additionalNotes TEXT,
            dataPoints INTEGER,
            gasComposition TEXT,
            coolingMethod TEXT,
            annealingTemp REAL
        ) """
        self.cur.execute(sampleMDTable)

        # Create Gas Composition Table
        gasCompTable = """CREATE TABLE gasCompositions (
            gasComposition TEXT PRIMARY KEY
        )"""
        self.cur.execute(gasCompTable)

        # Create Cooling Method Table
        coolingMethodTable = """CREATE TABLE coolingMethod (
            coolingMethod TEXT PRIMARY KEY
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
            sampleID TEXT PRIMARY KEY,
            specie TEXT NOT NULL,
            FOREIGN KEY (specie) REFERENCES species(specie)
        )"""
        self.cur.execute(intSpeciesTable)

    def insertSampleData(self, sampleID, simsData):
        self.cur.execute("INSERT INTO sampleData (sampleID, simsData) VALUES (?,?)",
            (sampleID, simsData))
    
    def insertSampleMetadata(self, sampleID, sputteringRate, annealingTime, additionalNotes, dataPoints , gasComposition , coolingMethod, annealingTemp):
        self.cur.execute("INSERT INTO sampleMetadata (sampleID, sputteringRate, annealingTime, additionalNotes, dataPoints , gasComposition , coolingMethod, annealingTemp) VALUES (?,?,?,?,?,?,?,?,)", (sampleID, sputteringRate, annealingTime, additionalNotes, dataPoints , gasComposition , coolingMethod, annealingTemp))
    
    def insertGasComp(self, gasComposition):
        self.cur.execute("INSERT INTO gasCompositions (gasComposition) VALUES (?)", (gasComposition))

    def insertCoolingMethod(self, coolingMethod):
        self.cur.execute("INSERT INTO coolingMethod (coolingMethod) VALUES (?)", (coolingMethod))

    def insertAnnealingTemp(self, temperature):
        self.cur.execute("INSERT INTO annealingTemp (temperature) VALUES (?)", (temperature))

    def insertSpecies(self, specie):
        self.cur.execute("INSERT INTO species (specie) VALUES (?)", (specie)) 

    def insertSpecies(self, sampleID, specie):
        self.cur.execute("INSERT INTO intSpecies (sampleID, specie) VALUES (?,?)", (sampleID, specie))