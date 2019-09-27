import sqlite3
import os

DEFAULT_PATH = os.path.join(os.path.dirname(__file__), 'simsdatastore.sqlite3')

class dbUtils():
    def __init__(self):
        if not os.path.exists(DEFAULT_PATH) and not os.path.isfile(DEFAULT_PATH):
            self.createDB()

    def dbConnect(self, dbPath=DEFAULT_PATH):
        return sqlite3.connect(dbPath)

    # Create SQLite3 DB here
    def createDB(self):
        print("Creating database!!!")
        con = self.dbConnect()
        cur = con.cursor()

        # Create Sample Data Table
        sampleDataTable = """CREATE TABLE sampleData (
            sampleID TEXT PRIMARY KEY,
            simsData BLOB
        )"""
        cur.execute(sampleDataTable)
        
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
        cur.execute(sampleMDTable)

        # Create Gas Composition Table
        gasCompTable = """CREATE TABLE gasCompositions (
            gasComposition TEXT PRIMARY KEY
        )"""
        cur.execute(gasCompTable)

        # Create Cooling Method Table
        coolingMethodTable = """CREATE TABLE coolingMethod (
            coolingMethod TEXT PRIMARY KEY
        )"""
        cur.execute(coolingMethodTable)

        # Create Annealing Temperature Table
        annealingTempTable = """CREATE TABLE annealingTemp (
            temperature REAL PRIMARY KEY
        )"""
        cur.execute(annealingTempTable)

        # Create Species Table
        speciesTable = """CREATE TABLE species (
            specie TEXT PRIMARY KEY
        )"""
        cur.execute(speciesTable)

        # Create intermediate species table
        intSpeciesTable = """CREATE TABLE intSpecies (
            sampleID TEXT PRIMARY KEY,
            specie TEXT NOT NULL,
            FOREIGN KEY (specie) REFERENCES species(specie)
        )"""
        cur.execute(intSpeciesTable)

    try:
        def insertSampleData(self, sampleID, simsData):
            con = self.dbConnect()
            cur = con.cursor()
            cur.execute("INSERT INTO sampleData (sampleID, simsData) VALUES (?,?)", (sampleID, simsData))
        
        def insertSampleMetadata(self, sampleID, sputteringRate, annealingTime, additionalNotes, dataPoints , gasComposition , coolingMethod, annealingTemp):
            con = self.dbConnect()
            cur = con.cursor()
            cur.execute("INSERT INTO sampleMetadata (sampleID, sputteringRate, annealingTime, additionalNotes, dataPoints , gasComposition , coolingMethod, annealingTemp) VALUES (?,?,?,?,?,?,?,?,)", (sampleID, sputteringRate, annealingTime, additionalNotes, dataPoints , gasComposition , coolingMethod, annealingTemp))
        
        def insertGasComp(self, gasComposition):
            con = self.dbConnect()
            cur = con.cursor()
            cur.execute("INSERT INTO gasCompositions (gasComposition) VALUES (?)", (gasComposition))

        def insertCoolingMethod(self, coolingMethod):
            con = self.dbConnect()
            cur = con.cursor()
            cur.execute("INSERT INTO coolingMethod (coolingMethod) VALUES (?)", (coolingMethod))

        def insertAnnealingTemp(self, temperature):
            con = self.dbConnect()
            cur = con.cursor()
            cur.execute("INSERT INTO annealingTemp (temperature) VALUES (?)", (temperature))

        def insertSpecies(self, specie):
            con = self.dbConnect()
            cur = con.cursor()
            cur.execute("INSERT INTO species (specie) VALUES (?)", (specie)) 

        def insertSpecies(self, sampleID, specie):
            con = self.dbConnect()
            cur = con.cursor()
            cur.execute("INSERT INTO intSpecies (sampleID, specie) VALUES (?,?)", (sampleID, specie)) 
    except:
        print("Errortest")
            
        

        
