"""
    The main file for executing the initial version of the application.
"""
import time
import os
import pymysql #pylint: disable=E0401
import speech #pylint: disable=E0401


SENSOR_BASE_PATH = "/sys/bus/w1/devices/"

TEMPERATURE_SENSOR_PATH = SENSOR_BASE_PATH + "28-000004fd2ca3"
TEMPERATURE_SENSOR_FILE = TEMPERATURE_SENSOR_PATH + "/w1_slave"

SERVER_NOTIFICATION_PATH = "/var/www/html/notifications"


os.system('modprobo w1-gpio')
os.system('modprobe w1-therm')

DB_CONNECTION = pymysql.connect("127.0.0.1", "root", "RaspberryVV", "testdb")
DB_CURSOR = DB_CONNECTION.cursor()


def read_temp_raw():
    """Reads the raw temperature"""
    temperature_file = open(TEMPERATURE_SENSOR_FILE, 'r')
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

    query = "INSERT INTO temperatures (temperature) VALUES ('%f');" % (temp)

    try:
        DB_CURSOR.execute(query)
        DB_CONNECTION.commit()
        speech.say("logged temperature of " + str(round(temp, 2)) + " degrees celcius.")
    except Exception as exception:
        print("aiai, rollback -", exception)
        DB_CONNECTION.rollback()
