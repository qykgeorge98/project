import psutil
import time

# Get initial disk I/O counters
disk_io_counters_start = psutil.disk_io_counters()

# Wait for a few seconds
time.sleep(5)

# Get disk I/O counters after waiting
disk_io_counters_end = psutil.disk_io_counters()

# Compute the difference in CPU and disk I/O counters and the time interval
read_bytes = disk_io_counters_end.read_bytes - disk_io_counters_start.read_bytes
write_bytes = disk_io_counters_end.write_bytes - disk_io_counters_start.write_bytes
time_diff = time.monotonic() - disk_io_counters_start.__getattribute__("busy_time")

# Compute the CPU utilization and read/write bytes per second
read_bytes_per_sec = read_bytes / time_diff
write_bytes_per_sec = write_bytes / time_diff

# Estimate energy consumption
energy_consumption = 1.36 * psutil.cpu_percent() + 0.22 * read_bytes_per_sec + 0.10 * write_bytes_per_sec

print("Estimated energy consumption: %.2f W" % energy_consumption)
