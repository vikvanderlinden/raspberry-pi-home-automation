import pymysql

DATABASE = pymysql.connect("127.0.0.1", "root", "RaspberryVV", "testdb")

CURSOR = DATABASE.cursor()

CURSOR.execute("SELECT temperature, note, time FROM temperatures")

for row in CURSOR.fetchall():
    temp = str(row[0])
    note = str(row[1])
    time = str(row[2])

    print(temp, note, time, sep=' - ')

CURSOR.close()
DATABASE.close()
