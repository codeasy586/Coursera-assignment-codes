import sqlite3

# creating a database and connecting it with the program
conn = sqlite3.connect('newassndb.sqlite')
cur = conn.cursor()

#dropping tables if exists
cur.execute('''
DROP TABLE IF EXISTS Counts''')

#CREATING RELEVANT table
cur.execute('''
CREATE TABLE Counts(org TEXT, count INTEGER)''')

#opening the file and writing and then reading it from the database
fname = input('Enter file name: ')
if(len(fname)<1): fname = 'mbox.txt'
fh = open(fname)
for line in fh:
    if not line.startswith('From'): continue
    piece = line.split()
    if(len(piece)>3):
     spl = piece[1]
     spl2 = spl.split('@')
     org = spl2[1]
     cur.execute('SELECT count FROM Counts WHERE org = ? ', (org, ))
     row = cur.fetchone()
     if row is None:
         cur.execute('INSERT INTO Counts(org,count) VALUES(?,1)', (org, ))
     else:
         cur.execute('UPDATE Counts SET count = count + 1 WHERE org = ? ', (org, ))
    else:
        continue
conn.commit()

#finally reading from the database
sqlstr = 'SELECT org,count FROM Counts ORDER BY count DESC'
for row in cur.execute(sqlstr):
    print(str(row[0]),row[1])
cur.close()
