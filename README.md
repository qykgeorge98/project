# project

# Read_LightAcceleration.py
1. Open a serial port connection using the serial.Serial() function. **The port name, baud rate and timeout need to be specified**. The baud rate is configured in the SmartRF Studio software.
2. **ls /dev/serial/by-id/** is used to specify the port name connected to the Raspberry Pi.
3. The code establishes a connection to an MySQL database using the pymysql.connect() function. 
4. db='project', table = 'test'. **Change the information according to your own database**.
5. Create the "test" table if it doesn't exist.
6. Define variables for data storage: The variables light, motion_X, motion_Y, and motion_Z are initialized to None. These variables will hold the data read from the serial input.
7. Read data from serial input and insert into the database.
8. When reading data and storing data in the database, corresponding modifications need to be made. **It depends on the code inside the sender sensor written by Ambuj**.

    b'light=278.40 lux\n'
    
    b'motion: X=0.16 \n'
    
    b'motion: Y=0.10 \n'
    
    b'motion: Z=0.87 \n'
9. for i in range(50): Read 50 groups of data. for j in range(4): Four lines as one group.
10. Insert data into the database: The code constructs an SQL query using the variables light, motion_X, motion_Y, motion_Z, and local_time and inserts the values into the "test" table using the cursor.execute() function. The changes are committed to the database using db.commit().
11. Close the cursor and database connection.


# Plot_LightAcceleration.py
1. motion_x = [row[2]/9.8 for row in rows] # Convert to g
2. time = [0, 0.5] # Set the initial time to 0 and 0.5. Because **we set to receive two sets of acceleration and light data every second**. Therefore, Set the initial time to 0 and 0.5.
3. When plotting the data in the database, we need to make corresponding modifications according to our own needs.
4. Plot the light vs time graph and Plot the motion vs time graph. Use **basic Pyplot visualization method**.


# Read_Temperature.py
1. For the part that processes **raw input**, it also depends on the code in the transmitter sensor and **needs to be changed**.
2. My **sample input** here is: 

    b'NOK\r\n'
  
    b'OK\r\n'
  
    b'238\r\n'
  
    b'99\r\n'.
    **Ambuj sets** b'NOK\r\n' is a symbol of the completion of each set of data transmission, and b'OK\r\n' is a symbol of the start of each set of data transmission.
  
3. cursor.rowcount == 100: Exit the loop after 100 temperature values are stored in the database。
4. temperature = round(val / 65535 * 160 - 40, 4). I mentioned in the paper that the temperature processing part is also initially configured in the Backscatter Sensor. We need to process the obtained 238 and 99, which is explained in the paper. Similarly, this part of the code also **needs to be changed** according to the actual situation.


# Plot_Temperature.py
**Similar to # plot_LightAcceleration**


# image.py
1. image.py is an E-paper official .py file provided by pimoroni.com/impression. **Watch the Tutorial I mentioned below, you will understand the basic use of E-Paper**.
2. Youtube Totorial: Set Up a 7 Colour E-Ink Display For Raspberry Pi | Inky Impression 5.7" HAT.
    **https://www.youtube.com/watch?v=daO46JaVHOs&t=200s**
3. Put image.py inside the same folder as other .py files.


# EPaperTemperature.py
1. In order to obtain Temperature.png, we need to run Plot_Temperature.py first.
2. Generate the plots folder:
    if not os.path.exists('plots'):
    os.makedirs('plots')
3. Generate a Temperature.png file:
    fig.write_image(
    "plots/Temperature.png")
4. To display an image on E-Paper, call a line of code: **os.system("python image.py ./plots/Temperature.png")**
5. Similarly, Light and Acceleration can also be displayed on E-Paper, the same operations.


# energyConsumption.py
1. The code is using the psutil library to measure disk I/O counters and compute the estimated energy consumption based on CPU utilization and read/write bytes per second. It uses the disk_io_counters() function to get the initial and final disk I/O counters, and the time.sleep() function to wait for a few seconds between the measurements.
2. Get the initial disk I/O counters: disk_io_counters_start = psutil.disk_io_counters()
3. Get the disk I/O counters after waiting: disk_io_counters_end = psutil.disk_io_counters()
4. Compute the difference in CPU and disk I/O counters and the time interval: 

    read_bytes = disk_io_counters_end.read_bytes - disk_io_counters_start.read_bytes
    
    write_bytes = disk_io_counters_end.write_bytes - disk_io_counters_start.write_bytes
    
    time_diff = time.monotonic() - disk_io_counters_start.__getattribute__("busy_time")
5. Compute the read/write bytes per second: 

    read_bytes_per_sec = read_bytes / time_diff
    
    write_bytes_per_sec = write_bytes / time_diff
6. Estimate energy consumption using a weighted sum of CPU utilization and read/write bytes per second: energy_consumption = 1.36 * psutil.cpu_percent() + 0.22 * read_bytes_per_sec + 0.10 * write_bytes_per_sec
7. Print the estimated energy consumption in Watt: print("Estimated energy consumption: %.2f W" % energy_consumption)


