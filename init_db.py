#adds sqlite3
import sqlite3

#creates database
connection = sqlite3.connect('database.db')

#opens schema file
with open('schema.sql') as f:
    connection.executescript(f.read())

#updates and closes schema file
connection.commit()
connection.close()