import serial

ser = serial.Serial("/dev/serial/by-id/usb-Texas_Instruments_XDS110__03.00.00.18__Embed_with_CMSIS-DAP_L201A07F-if00",
                    baudrate=115200, timeout=3.0)
ser.isOpen()

for i in range(20):
    x = ser.readline()
    data_pre = str(x)
    if 'NOK' in data_pre or 'OK' in data_pre:
        pass
    else:
        if len(data_pre) == 8:
            print(data_pre[2:3])
        else:
            print(data_pre[2:4])

# usb-Texas_Instruments_XDS110__03.00.00.18__Embed_with_CMSIS-DAP_L201A07F-if00
# usb-Texas_Instruments_XDS110__03.00.00.18__Embed_with_CMSIS-DAP_L201A07F-if03





