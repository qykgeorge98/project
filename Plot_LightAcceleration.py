import pymysql
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime

pymysql.install_as_MySQLdb()

# Connect to the database
db = pymysql.connect(host='localhost', user='root', password='qyk123123', db='project')
cursor = db.cursor()

# Get the data from the database
cursor.execute("SELECT * FROM test")
rows = cursor.fetchall()

# Extract the data into separate lists
light = [row[1] for row in rows]
motion_x = [row[2]/9.8 for row in rows] # Convert to g
motion_y = [row[3]/9.8 for row in rows] # Convert to g
motion_z = [row[4]/9.8 for row in rows] # Convert to g
time = [0, 0.5] # Set the initial time to 0 and 0.5
for i in range(2, len(rows)):
    t1 = datetime.strptime(rows[i][5], "%Y-%m-%d %H:%M:%S")
    t2 = datetime.strptime(rows[i-2][5], "%Y-%m-%d %H:%M:%S")
    diff = t1 - t2 # Calculate the time difference
    if diff.total_seconds() >= 0.5:
        time.append(time[-1] + 0.5) # Add 0.5 seconds to the previous time
    else:
        time[-1] += diff.total_seconds() # Add the time difference to the previous time

# Plot the light vs time graph
fig, ax = plt.subplots()
ax.plot(time, light, marker='o', markerfacecolor='blue', markersize=5)
ax.set_xlabel('Time (s)')
ax.set_ylabel('Light (lux)')
ax.set_title('Light vs Time')
ax.grid(True)
plt.show()

# Plot the motion vs time graph
fig, axs = plt.subplots(3, 1, sharex=True)
axs[0].plot(time, motion_x, marker='o', markerfacecolor='blue', markersize=5, label='Motion X')
axs[1].plot(time, motion_y, marker='o', markerfacecolor='blue', markersize=5, label='Motion Y')
axs[2].plot(time, motion_z, marker='o', markerfacecolor='blue', markersize=5, label='Motion Z')
axs[0].set_ylabel('Motion_X (g)')
axs[1].set_ylabel('Motion_Y (g)')
axs[2].set_ylabel('Motion_Z (g)')
axs[2].set_xlabel('Time (s)')
fig.suptitle('Acceleration vs Time')
for ax in axs:
    ax.grid(True)
    ax.legend()
    ax.axhline(y=0, color='k')
    ax.xaxis.set_tick_params(which='both', labelbottom=True)
    ax.yaxis.set_tick_params(which='both', labelleft=True)
plt.show()

cursor.close()
db.close()
