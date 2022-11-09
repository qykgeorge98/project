import serial

ser = serial.Serial("/dev/serial/by-id/usb-Texas_Instruments_XDS110__03.00.00.18__Embed_with_CMSIS-DAP_L201A07F-if00",
                    baudrate=115200, timeout=3.0)
ser.isOpen()

while 1:
    x = ser.readline()
    print(x)

# usb-Texas_Instruments_XDS110__03.00.00.18__Embed_with_CMSIS-DAP_L201A07F-if00
# usb-Texas_Instruments_XDS110__03.00.00.18__Embed_with_CMSIS-DAP_L201A07F-if03




