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