
## TODO: this should not run. But may be used as inspiration on how to implement further on the planthouseHub
import bluetooth
import logging
import sqlite3
import time
import numpy as np
from scipy.interpolate import interp1d

logging.basicConfig(filename='/var/log/bluetooth_sensor.log', level=logging.INFO)

def log_sensor_data(sensor_name, sensor_address, data):
    conn = sqlite3.connect('/home/pi/DielsiGarden/sensor_data.db') ## This is nit in the repo
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS sensor_data (
            id INTEGER PRIMARY KEY,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            sensor_name TEXT,
            sensor_address TEXT,
            data REAL
        )
    ''')
    cursor.execute('''
        INSERT INTO sensor_data (sensor_name, sensor_address, data)
        VALUES (?, ?, ?)
    ''', (sensor_name, sensor_address, data))
    conn.commit()
    conn.close()

def find_sensors():
    nearby_devices = bluetooth.discover_devices(duration=8, lookup_names=True, flush_cache=True, lookup_oui=False)
    return nearby_devices

def interpolate_data(sensor_name):
    conn = sqlite3.connect('/home/pi/repos/DielsiGarden/sensor_data.db')
    cursor = conn.cursor()
    cursor.execute('SELECT timestamp, data FROM sensor_data WHERE sensor_name = ? ORDER BY timestamp DESC LIMIT 10', (sensor_name,))
    rows = cursor.fetchall()
    conn.close()
    
    if len(rows) < 2:
        return None  # Not enough data for interpolation
    
    times = [time.mktime(time.strptime(row[0], '%Y-%m-%d %H:%M:%S')) for row in rows]
    values = [row[1] for row in rows]
    poly = np.polyfit(times, values, 2)  # Polynomial interpolation
    poly_interp = np.poly1d(poly)
    current_time = time.mktime(time.gmtime())
    interpolated_value = poly_interp(current_time)
    
    return interpolated_value

try:
    while True:
        sensors = find_sensors()
        for addr, name in sensors:
            # Simulated sensor data; replace this with actual sensor reading logic
            data = 42.0
            logging.info(f"Sensor {name} found with address {addr} and data {data}")
            log_sensor_data(name, addr, data)
            interpolated_value = interpolate_data(name)
            if interpolated_value is not None:
                logging.info(f"Interpolated value for {name}: {interpolated_value}")
        time.sleep(1800)  # Sleep for 30 minutes
except KeyboardInterrupt:
    logging.info("Stopped Bluetooth scanning")
