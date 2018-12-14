import os
import time
import pymysql

os.system('modprobo w1-gpio')
os.system('modprobe w1-therm')

base_dir = '/sys/bus/w1/devices/'
device_folder = base_dir + '28-000004fd2ca3'
device_file = device_folder + '/w1_slave'

db = pymysql.connect("127.0.0.1", "root", "RaspberryVV", "testdb")
cur = db.cursor()

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    
    return lines

def current_temperature():
    lines = read_temp_raw()
    
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()

    equals_pos = lines[1].find('t=')

    if equals_pos != -1:
        temp_string = lines[1][equals_pos + 2:]
        temp_c = float(temp_string) / 1000

        return temp_c

    return False

def log_temperature():
    temp = current_temperature()

    sql = "INSERT INTO temperatures (temperature) VALUES ('%f');" % (temp)

    try:
        cur.execute(sql)
        db.commit()
    except Exception as e:
        print("aiai, rollback -", e)
        db.rollback()

while True:
    try:
        log_temperature()
        print("Logged temperature")
        time.sleep(1200)
    except:
        cur.close()
        db.close()

