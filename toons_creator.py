#!/usr/bin/python

""" python creator for toons sqlite3 database """

# Import the required Python module
import sqlite3

# Create the database, a connection to it and a cursor
connection = sqlite3.connect('toons.db')
cursor = connection.cursor()

# Execute the SQLite statement to create the CDs table
cursor.execute("""
CREATE TABLE WB (
CDID integer primary key autoincrement,
Title varchar(50),
Char1 varchar(30),
Char2 varchar(30),
Char3 varchar(30),
Char4 varchar(30),
Director varchar(30),
Type varchar(10),
RelDateTxt varchar(30),
RelDateJul real,
ViewDateTxt varchar(30),
ViewDateJul real,
Page int,
Source varchar(50)
)""")

# Populate the table with some data...
# cursor.execute("""
# INSERT INTO WB VALUES (
# null,
# 'Hare Lift', 
# 'Bugs Bunny',
# 'Yosemite Sam',
# '',
# '',
# 'Freleng'
# 'LT' 
# date('1952-12-20'), 
# julianday('1952-12-20'),
# date('now'),
# julianday('now'),
# 243,
# 'www.supercartoons.net'
# )""")

# Commit the transaction and close the connection
connection.commit()
cursor.close()
connection.close()
