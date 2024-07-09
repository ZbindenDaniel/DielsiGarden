import RPi.GPIO as GPIO
import sqlite3
import sys
import logging
import time
import json
import numpy as np

# Load configuration
with open('/home/pi/repos/DielsiGarden/config.json', 'r') as f:
    config = json.load(f)

relay_pins = config['relay_pins']
thresholds = config['thresholds']
hold_times = config['hold_times']

GPIO.setmode(GPIO.BCM)
GPIO.setup(relay_pins['relay1'], GPIO.OUT)
GPIO.setup(relay_pins['relay2'], GPIO.OUT)

logging.basicConfig(filename='/home/pi/repos/DielsiGarden/logs/relay_control.log', level=logging.INFO)

def switch_relay(pin, state):
    GPIO.output(pin, state)
    logging.info(f"Relay {pin} switched to {'ON' if state else 'OFF'}")

def get_interpolated_sensor_data(sensor_name):
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

if __name__ == "__main__":
    try:
        sensor_name = "YourSensorName"  # Replace with your actual sensor name
        data = 7 #TODO: get_interpolated_sensor_data(sensor_name)
        if data is not None:
            logging.info(f"Interpolated data for {sensor_name}: {data}")
            
            # Check the sensor data and control the relays accordingly
            if data < thresholds['relay1']['min']:  # Example condition for relay 1
                switch_relay(relay_pins['relay1'], GPIO.HIGH)
                time.sleep(hold_times['relay1'])  # Keep relay on for desired duration
                switch_relay(relay_pins['relay1'], GPIO.LOW)
            elif data > thresholds['relay2']['max']:  # Example condition for relay 2
                switch_relay(relay_pins['relay2'], GPIO.HIGH)
                time.sleep(hold_times['relay2'])  # Keep relay on for desired duration
                switch_relay(relay_pins['relay2'], GPIO.LOW)
            
    except KeyboardInterrupt:
        GPIO.cleanup()
        logging.info("Cleaned up GPIO")
