import serial
import pymysql
import time

ser = serial.Serial("/dev/serial/by-id/usb-Texas_Instruments_XDS110__03.00.00.22__Embed_with_CMSIS-DAP_L1061-if00",
                      bau12drate=115200, timeout=3.0)  # # Open the serial port, followed by the serial port configuration
ser.isOpen()

pymysql.install_as_MySQLdb()

db = pymysql.connect(host='localhost', user='root', password='qyk123123',
                     db='project')  # Open the database, configure the database
cursor = db.cursor()  # database operations

# Check if "test" table exists
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
table_names = [table[0] for table in tables]
if "test" not in table_names:
    # Table doesn't exist, create it
    creatTab = """CREATE TABLE test( # create table
        DATA_ID INT NOT NULL AUTO_INCREMENT,
        Light FLOAT,
        Motion_X FLOAT,
        Motion_Y FLOAT,
        Motion_Z FLOAT,
        TIME CHAR(50),
        PRIMARY KEY (DATA_ID))"""
    cursor.execute(creatTab)
    db.commit()

# Define variables to store data
light = None
motion_X = None
motion_Y = None
motion_Z = None

# Read data from serial input and insert into database table
for i in range(50):
    # Read four rows of data
    for j in range(4):
        x = ser.readline().decode('utf-8')
        if x.startswith('light='):
            light = float(x.split('=')[1].split(' ')[0])
        elif x.startswith('motion: X='):
            motion_X = float(x.split('=')[1].split(' ')[0].replace('-', ''))
        elif x.startswith('motion: Y='):
            motion_Y = float(x.split('=')[1].split(' ')[0].replace('-', ''))
        elif x.startswith('motion: Z='):
            motion_Z = float(x.split('=')[1].split(' ')[0].replace('-', ''))
    local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    sql = "INSERT INTO test(Light, Motion_X, Motion_Y, Motion_Z, TIME)VALUES('%s','%s','%s','%s','%s')" \
          % (light, motion_X, motion_Y, motion_Z, local_time)
    cursor.execute(sql)  # execute sql sentence
    db.commit()  # commit the database

cursor.close()
db.close()
