import os
import time
import pymysql

os.system('modprobo w1-gpio')
os.system('modprobe w1-therm')

BASE_DIRECTORY = '/sys/bus/w1/devices/'
DEVICE_FOLDER = BASE_DIRECTORY + '28-000004fd2ca3'
DEVICE_FILE = DEVICE_FOLDER + '/w1_slave'

DATABASE = pymysql.connect("127.0.0.1", "root", "RaspberryVV", "testdb")
CURSOR = DATABASE.cursor()

def read_temp_raw():
    """Reads the raw temperature"""
    temperature_file = open(DEVICE_FILE, 'r')
    lines = temperature_file.readlines()
    temperature_file.close()

    return lines

def current_temperature():
    """Reads the current temperature"""
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
    """Logs the temperature"""
    temp = current_temperature()

    sql = "INSERT INTO temperatures (temperature) VALUES ('%f');" % (temp)

    try:
        CURSOR.execute(sql)
        DATABASE.commit()
    except Exception as e:
        print("aiai, rollback -", e)
        DATABASE.rollback()

while True:
    try:
        log_temperature()
        print("Logged temperature")
        time.sleep(1200)
    except Exception:
        CURSOR.close()
        DATABASE.close()
