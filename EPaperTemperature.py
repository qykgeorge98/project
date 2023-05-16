import os
import pymysql
import matplotlib.pyplot as plt
from datetime import datetime

pymysql.install_as_MySQLdb()

db = pymysql.connect(host='localhost', user='root', password='qyk123123', db='project')
cursor = db.cursor()

# Retrieve the temperature and time data from the database
cursor.execute("SELECT TEMPERATURE, TIME FROM test1")
data = cursor.fetchall()

# Initialize the time and temperature lists
time_list = []
temp_list = []

# Loop through the data and extract the time and temperature values
for i in range(len(data)):
    temp_list.append(data[i][0])
    if i == 0:
        time_list.append(0)
    else:
        time1 = datetime.strptime(data[0][1], "%Y-%m-%d %H:%M:%S")
        time2 = datetime.strptime(data[i][1], "%Y-%m-%d %H:%M:%S")
        delta = (time2 - time1).total_seconds()
        time_list.append(delta)

# Plot the temperature vs time graph
plt.plot(time_list, temp_list, marker='o', markerfacecolor='blue', markersize=5, label='Temperature vs Time')
plt.xlabel('Time (s)')
plt.ylabel('Temperature (°C)')
plt.title('Temperature vs Time')
plt.grid(True)
plt.legend()
plt.show()

if not os.path.exists('plots'):
    os.makedirs('plots')

fig.write_image(
    "plots/Temperature.png")

os.system("python image.py ./plots/Temperature.png")

cursor.close()
db.close()
