import ssl
import sys
import re
import os.path
import argparse
import time
import random
import requests
import json
from configparser import ConfigParser
from datetime import datetime
from miflora.miflora_poller import MiFloraPoller, MI_BATTERY, MI_LIGHT, MI_CONDUCTIVITY, MI_MOISTURE, MI_TEMPERATURE
from btlewrap.bluepy import BluepyBackend
import collections
import logging

class IotDevice:
    def __init__(self, config):
        self.id = config['deviceId']
        self.name = config['name']
        self.mac = config['mac']
        self.poller = MiFloraPoller(config['mac'], BluepyBackend)
    
    def getSensorReadings(self):
        return {
                "Temperature": random.randint(-15,38),
                "humidity": random.randint(0,100),
                "pressure": random.randint(700,1500),
                "illuminance": random.randint(700,1500),
                "uva": random.randint(700,1500),
                "uvb": random.randint(10,2000),
                "uvIndex": random.randint(10,2000),
                "BatteryLevel": random.randint(1,100),
                "DeviceId":self.id,
                "TimeStamp":datetime.now().strftime("%d.%m.%Y - %H:%M:%S")
            }
        
        data = {
                "Temperature": self.poller.parameter_value(MI_TEMPERATURE),
                "humidity": self.poller.parameter_value(MI_MOISTURE),
                "pressure": random.randint(700,1500),
                "illuminance": self.poller.parameter_value(MI_LIGHT),
                "uva": self.poller.parameter_value(MI_CONDUCTIVITY),
                "uvb": random.randint(10,2000),
                "uvIndex": random.randint(10,2000),
                "BatteryLevel": self.poller.parameter_value(MI_BATTERY),
                "DeviceId":self.id
            }
        return data 

sensors = []
def initSensors():
    while True:
        try:
            deviceConfigs = json.loads(config['Device'].get('Devices'))
            for deviceConfig in deviceConfigs:
                sensors.append(IotDevice(deviceConfig))
            break
        except Exception as err:
            logging.warning(f"Failed to initialize sensors. {err=} {type(err)=}. Retrying in 10 seconds...")
            time.sleep(10)

headers = {
        'Connection': 'close',
        'Content-type': 'application/json',
        'Host': 'api.dzb-projects.ch',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36 OPR/94.0.0.0'
        }

def authenticate():
    while True:
        try:
            login_url = config.get('Settings', 'BaseUrl') + "auth/loginAstestuser"
            res = login_response = requests.post(login_url, headers=headers)
            if res.status_code == 200:
                token = login_response.json()['jwtBearer']
                headers['Authorization'] = f'{token}'
                return True
            else:
                logging.warning(f"Failed to authenticate. {res.status_code=}, {res.content=}.")
                return False
        except Exception as err:
            logging.warning(f"Failed to authenticate. {err=} {type(err)=}.")
            return False

def DisectResponse(response):
    print(response) # TODO: foreach sensor a json is returned. replace IotNodeSettingsModel from api with structure from .ini and replace .ini by json

DATA_FILE = '/home/pi/repos/DielsiGarden/data/sensors.json'

# Define the maximum number of data sets you want to keep
N = 145 # script running every 20 minutes, for 24h, 2 sensors 

# Function to load data from file
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
data_deque = load_data_from_file()

# Function to save data to file
def save_data_to_file(data_deque):
    with open(DATA_FILE, 'w') as file:
        json.dump(list(data_deque), file)
        
def main():

    # url
    endPoint = str(config['Settings'].get('BaseUrl')) + 'Data' # TODO: to config
    authenticated = False

    # device
    # deviceConfigs = json.loads(config['Device'].get('Devices'))

    initSensors()
    authenticationAttempts = 0
    sensorReadingAttempts = 0
    uploadCount = 0
    try:
        for sensor in sensors:
            data = sensor.getSensorReadings()
            data_deque.append(data)
            save_data_to_file(data_deque)
            # TODO: the authentication part is optional for local data storage. so the data is collected and the comes the authentication. or maybe the authentication belongs into a whole new file
        #     while not authenticated:
        #         authenticationAttempts += 1
        #         if authenticationAttempts >= config['Settings'].getint('MaxAuthenticationAttempts'):
        #             break
        #         authenticated = authenticate()
        #         time.sleep(config['Settings'].getint('AuthenticationTimeout'))
        #     if authenticated:
        #         x = requests.post(endPoint, headers=headers, json=data)
        #         if x.status_code == 401:
        #             authenticated = False
        #         elif x.status_code == 422:
        #             print(x.text)
        #             # TODO: Often the timeout is not matched. so it would need a second try a little bit later, but only once or twice
        #         elif x.status_code != 200:
        #             logging.warning(f'{datetime.now()}: {x.status_code} - {x.text}')
        #         uploadCount = uploadCount + 1
        #         if uploadCount >= config['Settings'].getint('LogDataUploadCycle'):
        #             print("TODO: Upload Logfile and delete oldOne") # probably better to have in own loop or even service but first needs implemntation in API
        #     DisectResponse(res)
        # time.sleep(config['Settings'].getint('LoopTimeout'))
            
    except Exception as err:
        logging.critical(f"Unexpected {err=}, {type(err)=} - {err}")
        time.sleep(1)
        if sensorReadingAttempts >= config['Settings'].getint('MaxSensorReadingAttempts'):
            return
    print("Exit Program")

config = {}

if __name__ == "__main__":
    project_url = ""
    parser = argparse.ArgumentParser(description="Planthouse Hub", epilog='For further details see: ' + project_url)
    parser.add_argument('--config_dir', help='set directory where config.ini is located', default=sys.path[0])
    #parser.add_argument('--delay', help='set delay between sensor readings (in seconds)', type=int, default=300)
    args = parser.parse_args()

    # Load configuration file
    config_dir = args.config_dir

    config = ConfigParser(delimiters=('=', ), inline_comment_prefixes=('#'))
    config.optionxform = str
    try:
        logging.basicConfig(filename=os.path.join(config_dir, 'logs/planthouse.log'), encoding='utf-8', level=logging.DEBUG)
    except IOError:
        print("Cannot open logFile")
        sys.exit(1)
    try:
        with open(os.path.join(config_dir, 'planthouseHub.ini')) as config_file:
            config.read_file(config_file)

        main()

    except IOError:
        print('No configuration file "config.ini"')
        sys.exit(1)
    finally:
        logging.info("PlanthouseDevice stops execution")
        print("PlanthouseDevice stops execution")
        