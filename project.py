import serial
import pymysql
import time

log = 0
ser = serial.Serial("/dev/serial/by-id/usb-Texas_Instruments_XDS110__03.00.00.18__Embed_with_CMSIS-DAP_L201A07F-if00",
                    baudrate=115200, timeout=3.0)  # # Open the serial port, followed by the serial port configuration
ser.isOpen()

pymysql.install_as_MySQLdb()

db = pymysql.connect(host='localhost', user='root', password='123456',
                     db='test')  # Open the database, configure the database
cursor = db.cursor()  # database operations
cursor.execute("DROP TABLE IF EXISTS project")  # Recreate the table if it exists
creatTab = """CREATE TABLE project( # create table
    DATA_ID CHAR(20) NOT NULL,
    hex_number varchar(50) null,
    TIME CHAR(50))"""
cursor.execute(creatTab)  # execute database statement

for i in range(30):
    x = ser.readline()
    data_pre = str(x)
    if 'NOK' in data_pre or 'OK' in data_pre:
        pass
    else:
        log += 1  # log record + 1
        if len(data_pre) == 8:
            data = data_pre[2:3]
        else:
            data = data_pre[2:4]
        print(data)
        localtime = time.asctime(time.localtime(time.time()))  # time package operation, print local time
        local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # Format local time
        sql = "INSERT INTO project(DATA_ID, hex_number, TIME)VALUES('%d','%s','%s')" % (log, data, local_time)  # store in database
        cursor.execute(sql)  # execute sql sentence
        db.commit()  # commit the database

cursor.close()
db.close()

# usb-Texas_Instruments_XDS110__03.00.00.18__Embed_with_CMSIS-DAP_L201A07F-if00
# usb-Texas_Instruments_XDS110__03.00.00.18__Embed_with_CMSIS-DAP_L201A07F-if03
