CREATE TABLE SensorData (
    SequenceNumber INT NOT NULL AUTO_INCREMENT,
    Time DATETIME NOT NULL,
    SensorNodeID INT NOT NULL,
    EnergyReading INT NOT NULL,
    Temperature FLOAT,
    Humidity FLOAT,
    AccelerometerX FLOAT,
    AccelerometerY FLOAT,
    AccelerometerZ FLOAT,
    LightSensor FLOAT,
    PRIMARY KEY (SequenceNumber)
);

import mysql.connector
import matplotlib.pyplot as plt

# Connect to MySQL database
cnx = mysql.connector.connect(user='yourusername', password='yourpassword', host='localhost', database='yourdatabase')
cursor = cnx.cursor()

# Function to retrieve temperature data from database and plot it
def plot_temperature(start, end, axis):
    query = ("SELECT Time, Temperature FROM Temperature WHERE SequenceNumber BETWEEN %s AND %s")
    cursor.execute(query, (start, end))
    rows = cursor.fetchall()

    # Extract time and temperature data from rows
    times = [row[0] for row in rows]
    temperatures = [row[1] for row in rows]

    # Plot the data
    plt.plot(times, temperatures)
    plt.xlabel('Time')
    plt.ylabel('Temperature')
    plt.title('Temperature Data')
    plt.show()

# Example usage: plot temperature data for sensor ID 1234 between sequence numbers 100 and 200
plot_temperature(100, 200, 'Time')

# Close the database connection
cursor.close()
cnx.close()

