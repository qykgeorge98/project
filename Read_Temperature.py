import serial
import pymysql
import time

ser = serial.Serial("/dev/serial/by-id/usb-Texas_Instruments_XDS110__02.03.00.05__Embed_with_CMSIS-DAP_L201A07F-if00",
                    baudrate=115200, timeout=3.0)  # # Open the serial port, followed by the serial port configuration
ser.isOpen()

pymysql.install_as_MySQLdb()

db = pymysql.connect(host='localhost', user='root', password='qyk123123', db='project')
cursor = db.cursor()

# Check if "test2" table exists
cursor.execute("SHOW TABLES")
tables = cursor.fetchall()
table_names = [table[0] for table in tables]
if "test2" not in table_names:
    # Table doesn't exist, create it
    creatTab = """CREATE TABLE test2(
                  DATA_ID INT NOT NULL AUTO_INCREMENT,
                  TEMPERATURE FLOAT,
                  TIME CHAR(50),
                  PRIMARY KEY (DATA_ID))"""
    cursor.execute(creatTab)
    db.commit()

while True:
    # Read data from serial input
    x = ser.readline()

    # Convert the temperature values to float and store them in the database
    if x.startswith(b'OK\r\n'):
        temp1 = ser.readline().strip()
        temp2 = ser.readline().strip()

        if temp1.isdigit() and temp2.isdigit():
            hex1 = hex(int(temp1))[2:].zfill(2)
            hex2 = hex(int(temp2))[2:].zfill(2)
            hex_val = hex2 + hex1  # Swap the order of the bytes
            val = int(hex_val, 16)
            temperature = round(val / 65535 * 160 - 40, 4)
            local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
            sql = "INSERT INTO test2(TEMPERATURE, TIME) VALUES (%s, %s)"
            cursor.execute(sql, (temperature, local_time))
            db.commit()

    # Exit the loop after 100 temperature values are stored in the database
    if cursor.rowcount == 100:
        break

cursor.close()
db.close()

