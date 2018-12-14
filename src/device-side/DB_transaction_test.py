import pymysql

db = pymysql.connect("127.0.0.1", "root", "RaspberryVV", "testdb")

cur = db.cursor()

cur.execute("SELECT temperature, note, time FROM temperatures")

for row in cur.fetchall():
    temp = str(row[0])
    note = str(row[1])
    time = str(row[2])

    print(temp, note, time, sep=' - ')

cur.close()
db.close()
