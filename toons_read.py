#!/usr/bin/python

""" sqlite python read data from WB table in toons database """

# Import the required Python module
import sqlite3

SQL_BASE = 'SELECT * FROM WB '

def showMenu():
    show = True
    sql = ''
    while show:
        print "\n Options Menu"
        print "---------------------"
        print " A. Show All Records"
        print " B. Show Last 10 Records"
        print " C. Search By Title"
        print " D. Search By Director"
        print " E. Search By Character"
        print " F. Search By Year of Release"
        print " G. Search By Rating"
        print " H. Sort By Release Date"
        print " I. Sort By Viewing Date"
        print " J. Custom SQL Statement"
        print " K. Show Table Fields"
        print " Q. Quit"
        option = raw_input("\n Choose an option: ")
        if option == 'Q' or option == 'q':
            show = False
        elif option == 'A' or option == 'a':
            sql = SQL_BASE
            print "\n " + sql
            exeSQL(sql)
	elif option == 'B' or option == 'b':
	    sql = SQL_BASE
	    sql += "ORDER BY CDID DESC LIMIT 10"
	    print "\n " + sql
	    exeSQL(sql)
        elif option == 'c' or option == 'C':
            title = raw_input(" ENTER Title: ")
            sql = SQL_BASE + 'WHERE Title LIKE "%' + title + '%"'
            print "\n " + sql
            exeSQL(sql)            
        elif option == 'D' or option == 'd':
            director = raw_input(" ENTER Director: ")
            sql = SQL_BASE + 'WHERE Director LIKE "%' + director + '%"'
            sql += " ORDER BY RelDateTxt" 
            print "\n " + sql
            exeSQL(sql)
        elif option == 'E' or option == 'e':
            char = raw_input(" ENTER Character: ")
            sql = SQL_BASE + "WHERE Char1 LIKE '%" + char + "%'" 
            sql += " OR Char2 LIKE '%" + char + "%'"
            sql += " OR Char3 LIKE '%" + char + "%'"
            sql += " OR Char4 LIKE '%" + char + "%'"
            sql += " ORDER BY RelDateTxt"
            print "\n " + sql
            exeSQL(sql)
        elif option == 'F' or option == 'f':
            year = raw_input(" ENTER Year: ")
            sql = SQL_BASE + "WHERE RelDateTxt LIKE '%" + year + "%' ORDER BY RelDateTxt"
            print "\n " + sql
            exeSQL(sql)
        elif option == 'G' or option == 'g':
            while True:
                rate = raw_input(" ENTER Rating (1, 2, 3): ")
                if rate not in ['1', '2', '3']:
                    print " Invalid rating entered...try again"
                else:
                    break
            sql = SQL_BASE + "WHERE Rating=" + str(rate) + " ORDER BY RelDateTxt"
            print "\n " + sql
            exeSQL(sql)
        elif option == 'H' or option == 'h':
            sql = SQL_BASE + "ORDER BY RelDateTxt"
            print "\n " + sql
            exeSQL(sql)
        elif option == 'I' or option == 'i':
            sql = SQL_BASE + "ORDER BY ViewDateJul DESC"
            print "\n " + sql
            exeSQL(sql)
        elif option == 'J' or option == 'j':
            sql = raw_input(" ENTER SQL Statement: " + SQL_BASE)
            print "\n " + SQL_BASE + sql
            exeSQL(SQL_BASE + sql)
        elif option == 'K' or option == 'k':
            showTableFields()
        else:
            print "Invalid option entered..."
            
def showTableFields():
    print '\n WB Table Fields'
    print '-'*22
    lineText =  " CDID:        Integer\n"
    lineText += " Title:       Text\n"
    lineText += " Char1:       Text\n"
    lineText += " Char2:       Text\n"
    lineText += " Char3:       Text\n"
    lineText += " Char4:       Text\n"
    lineText += " Director:    Text\n"
    lineText += " Type:        Text\n"
    lineText += " RelDateTxt:  Text\n"
    lineText += " RelDateJul:  Real\n"
    lineText += " ViewDateTxt: Text\n"
    lineText += " ViewDateJul: Real\n"
    lineText += " Page:        Integer\n"
    lineText += " Source:      Text\n"
    lineText += " Rating:      Integer"
    print lineText
    print '-'*22

def showRecords(recordset):
    print '-'*80
    count = 0
    size = len(recordset)
    for record in recordset:
        lineText = " " + str(record[0]).ljust(5) # ID
        lineText += record[1][:29].ljust(31) # Title
        lineText += record[6].split()[-1].ljust(10) # Director
        lineText += record[8].ljust(12) # Release Date
        lineText += record[2].ljust(18) # Char1
        lineText += record[7] # Type
        print lineText
        lineText = " "*6 + record[13].ljust(31) # Source
        lineText += str(record[14]).ljust(10) # Rating
        lineText += record[10][0:10].ljust(12) # View Date
        if record[3] != '':
            lineText += record[3].ljust(18) # Char2
        else:
            lineText += ''.ljust(18)
        lineText += str(record[12]) # Ref. Page
        print lineText
        if record[4] != '':
            lineText = " "*59 + record[4] # Char3
            print lineText
        if record[5] != '':
            lineText = " "*59 + record[5] # Char4
            print lineText
        print '-'*80
	count += 1
        size -= 1
	if count > 11 and size > 0:
	    raw_input("\nPress ENTER to view next set of records ")
	    count = 0
	    print '\n' + '-'*80

def exeSQL(sql):
    try:
        cursor.execute(sql)
        recordset = cursor.fetchall()
        print "\n %d Records Returned" % len(recordset)
        showRecords(recordset)
    except sqlite3.OperationalError as e:
        print " ERROR: " + e.message
    finally:
        raw_input("\n Press 'ENTER' to show main menu...")
    
# Main program execution starts here

# Create the database, a connection to it and a cursor
connection = sqlite3.connect('toons.db')
cursor = connection.cursor()

showMenu()
    
# Close the connection
cursor.close()
connection.close()
