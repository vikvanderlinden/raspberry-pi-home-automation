import pymysql
import time
import os


sensor_base_path = "/sys/bus/w1/devices/"

temperature_sensor_path = sensor_base_path + "28-000004fd2ca3"
temperature_sensor_file = temperature_sensor_path + "/w1_slave"

server_notifications_path = "/var/www/html/notifications"


os.system('modprobo w1-gpio')
os.system('modprobe w1-therm')

db_connection = pymysql.connect("127.0.0.1", "root", "RaspberryVV", "testdb")
db_cursor = db_connection.cursor()


def read_temp_raw():
    f = open(temperature_sensor_file, 'r')
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
        db_cursor.execute(sql)
        db_connection.commit()
        say("logged temperature of " + str(round(temp, 2)) + " degrees celcius logged."
    except Exception as e:
        print("aiai, rollback -", e)
        db_connection.rollback()


