import datetime
import RPi.GPIO as GPIO
import sqlite3
import sys
import logging
import time
import json
import numpy as np
import random
import collections
import os
import pandas as pd

# Load configuration
with open('/home/pi/repos/DielsiGarden/config.json', 'r') as f:
    config = json.load(f)

relay_pins = config['relay_pins']
thresholds = config['thresholds']
hold_times = config['hold_times']

GPIO.setmode(GPIO.BCM)

logging.basicConfig(filename='/home/pi/repos/DielsiGarden/logs/relay_control.log', level=logging.INFO)

def switch_relay(pin, state):
    if state == GPIO.HIGH:
        GPIO.setup(pin, GPIO.IN)
    else:
        GPIO.setup(pin, GPIO.OUT)
        
    logging.info(f"Relay {pin} switched {'OFF' if state else 'ON'}")

DATA_FILE = '/home/pi/repos/DielsiGarden/data/sensors.json' # TODO: move tom common module or config

def get_interpolated_humidity(data_deque):
    df = pd.read_json(DATA_FILE)
    
    sensor_id = 1
    filtered_df = df[df['DeviceId'] == sensor_id]
    print(filtered_df)
    start_date = '16.07.2024 - 16:36:19'
    end_date = '16.07.2024 - 16:38:19'
    filtered_df = df[(df['DeviceId'] == sensor_id) & (df['TimeStamp'] >= start_date) & (df['TimeStamp'] <= end_date)]
    print(filtered_df)
    # conn = sqlite3.connect('/home/pi/repos/DielsiGarden/sensor_data.db')
    # cursor = conn.cursor()
    # cursor.execute('SELECT timestamp, data FROM sensor_data WHERE sensor_name = ? ORDER BY timestamp DESC LIMIT 10', (sensor_name,))
    # rows = cursor.fetchall()
    # conn.close()
    
    # if len(rows) < 2:
    #     return None  # Not enough data for interpolation
    
    times = [time.mktime(time.strptime(row[0], '%Y-%m-%d %H:%M:%S')) for row in rows]
    values = [row[1] for row in rows]
    poly = np.polyfit(times, values, 2)  # Polynomial interpolation
    poly_interp = np.poly1d(poly)
    current_time = time.mktime(time.gmtime())
    interpolated_value = poly_interp(current_time)
    
    return interpolated_value

# Function to load data from file
N = 145 # script running every 20 minutes, for 24h, 2 sensors 

def load_data_from_file():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, 'r') as file:
                data = json.load(file)
                return collections.deque(data, maxlen=N)
        except (FileNotFoundError, json.JSONDecodeError):
            return collections.deque(maxlen=N)
    else:
        return collections.deque(maxlen=N)

# Load existing data from file

if __name__ == "__main__":
    try:
        data_deque = load_data_from_file()
        data = get_interpolated_humidity(data_deque)
        now = datetime.datetime.now()
        if data is not None:
            logging.info(f"{now} - data for {sensor_name}: {data}")
            
            # Check the sensor data and control the relays accordingly
            if data < thresholds['relay1']['lower']:
                switch_relay(relay_pins['relay1'], GPIO.LOW)
            elif data > thresholds['relay1']['upper']:
                switch_relay(relay_pins['relay1'], GPIO.HIGH)
                
            if data < thresholds['relay2']['lower']:
                switch_relay(relay_pins['relay2'], GPIO.LOW)
            elif data > thresholds['relay2']['upper']:
                switch_relay(relay_pins['relay2'], GPIO.HIGH)
                
    except:
        GPIO.cleanup()
        logging.critical("Exception thrown")
