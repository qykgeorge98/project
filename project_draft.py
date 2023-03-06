import serial
import pymysql
import time
import plotly.graph_objects as go  # Import plotly underlying drawing library

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

for i in range(5): # Do data visualization part for 5 times

    '''
    The following is to read 30 sets of data from CC1310
    '''
    for i in range(30):
        x = ser.readline()
        data_pre = str(x)
        if 'NOK' in data_pre or 'OK' in data_pre:
            pass
        else:
            log += 1  # log record + 1
            if len(data_pre) == 8:
                data = data_pre[2:3]
                if data == '5':
                    continue
            else:
                data = data_pre[2:4]
            print(data)
            localtime = time.asctime(time.localtime(time.time()))  # time package operation, print local time
            local_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # Format local time
            sql = "INSERT INTO project(DATA_ID, hex_number, TIME)VALUES('%d','%s','%s')" % (log, data, local_time)  # store in database
            cursor.execute(sql)  # execute sql sentence
            db.commit()  # commit the database

    '''
    Read data from Database"test"
    '''
    test_li = test.values.tolist()  # read the data from the database named "test"
    result = []  # store values of the column
    for s_li in test_li:
        result.append(s_li[1])  # Add new numbers at the end of the second column of the array based on the input value on the CC1310
    data_id = [i for i in (1, len(result)+1)]

    '''
    For data visualization
    '''
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=data_id,
            y=result,
            mode="markers+lines+text",  # << layout
            text=result,  # << layout
            textposition="top center"  # << layout
        ))
    fig.update_layout(
        title="Data Visualization",
        xaxis=dict(title="data_id", nticks=13),
        yaxis=dict(title="HexNumValue", nticks=11, rangemode="tozero", range=(0, 50)),
        width=500,
        height=500
    )
    fig.show()

'''
Finish reading, storing, visualization
'''
cursor.close()
db.close()

# usb-Texas_Instruments_XDS110__03.00.00.18__Embed_with_CMSIS-DAP_L201A07F-if00
# usb-Texas_Instruments_XDS110__03.00.00.18__Embed_with_CMSIS-DAP_L201A07F-if03 
