#!/usr/bin/python

""" sqlite python add data to WB table in toon database """

# Import the required Python module
import sqlite3

# CONSTANTS
FIRST_YEAR = 1930
LAST_YEAR = 1988

def validateYMD(value, first, last, comment):
    try:
        intVal = int(value)
        if intVal in range(first, last+1):
            returnVal = True
        else:
            returnVal = False
            print comment
            print "Value not in range. Try again..."
    except:
        returnVal = False
        print comment
        print "Conversion to integer failed. Try again..." 
    return returnVal

# Create the database, a connection to it and a cursor
connection = sqlite3.connect('toons.db')
cursor = connection.cursor()
more = True

while more:
    # Prompt for cartoon information...
    title = raw_input("\nTitle: ")
    try:
        cursor.execute('SELECT * FROM WB WHERE Title LIKE "%s"' % title)
        recordset = cursor.fetchall()
    except sqlite3.OperationalError as e:
        print " ERROR: " + e.message
        break
    if len(recordset) > 0:
        print 'ERROR: "%s" is already in the database...Try again' % title
        continue 
    chars = []
    for num in range(1,5):
        chars.append(raw_input("Character %d (ENTER for none): " % num))
    director = raw_input("Director: ")
    filmType = raw_input("Type (MM, LT, Other): ")
    while True:
        releaseYear = raw_input("'%s' year of release (1930-1988): " % title)
        verify = validateYMD(releaseYear, 1930, 1988, "Invalid year entered.")
        if verify:
            break
    while True:
        releaseMonth = raw_input("'%s' month of release (1-12): " % title) 
        verify = validateYMD(releaseMonth, 1, 12, "Invalid month entered.")
        if verify:
            break
    while True:
        releaseDay = raw_input("'%s' day of release (1-31): " % title)
        verify = validateYMD(releaseDay, 1, 31, "Invalid day entered.")
        if verify:
            break
         
    releaseDate = "%s-%s-%s" % (releaseYear, releaseMonth.rjust(2,'0'), releaseDay.rjust(2,'0'))

    # viewNow = raw_input("Set view date to now (y/n)? ")
    # if viewNow == 'n' or viewNow == 'N':
    #     while True:
    #         viewYear = raw_input("'%s' year of viewing (1980-2025): " % title)
    #         verify = validateYMD(viewYear, 1980, 2025, "Invalid year entered.")
    #         if verify:
    #             break
    #     while True:
    #         viewMonth = raw_input("'%s' month of viewing (1-12): " % title)
    #         verify = validateYMD(viewMonth, 1, 12, "Invalid month entered.")
    #         if verify:
    #             break
    #     while True:
    #         viewDay = raw_input("'%s' year of viewing (1-31): " % title)
    #         verify = validateYMD(viewDay, 1, 31, "Invalid day entered.")
    #         if verify:
    #             break
    #     viewDate = "%s-%s-%s" % (viewYear, viewMonth.rjust(2,'0'), viewDay.rjust(2,'0'))
    # else:
    #     viewDate = 'now'
    
    page = raw_input("Reference Book Page Number: ")
    source = raw_input("Viewing Source: ")
    while True:
        srating = raw_input("Rating (1 to 3): ")
        try:
            rating = int(srating)
            if rating in (1,2,3):
                break
            else:
                print "Invalid Rating - must be 1, 2, or 3 - try again"
        except:
            print "String to integer conversion failed - try again"
    
    print "\nReview Data"
    print "-----------"
    print "Title:        %s" % title
    print "Character 1:  %s" % chars[0]
    print "Character 2:  %s" % chars[1]
    print "Character 3:  %s" % chars[2]
    print "Character 4:  %s" % chars[3]
    print "Director:     %s" % director
    print "Type:         %s" % filmType.upper()
    print "Release Date: %s" % releaseDate
    print "Page Number:  %d" % int(page)
    print "Source:       %s" % source
    print "Rating:       %d" % rating
    cont = raw_input("Commit data to the database (y/n)? ")

    if cont == 'y' or cont == 'Y':
        # Populate the table with the data...
        cursor.execute("""
        INSERT INTO WB VALUES (
        null,
        "%s", 
        "%s",
        "%s",
        "%s",
        "%s",
        "%s",
        "%s", 
        date("%s"), 
        julianday("%s"),
        datetime('now','localtime'),
        julianday('now','localtime'),
        %d,
        "%s",
        %d
        )""" % (title, chars[0], chars[1], chars[2], chars[3], director, filmType.upper(), 
                releaseDate, releaseDate, int(page), source, rating))
        # Commit the transaction
        connection.commit()
        print "Database write complete."
    else:
        print "Data not committed to database."
    
    cont = raw_input("\nEnter more data (y/n)? ")
    if cont == 'Y' or cont == 'y':
        more = True
    else:
        more = False
    
# Close the connection
cursor.close()
connection.close()


