import json
import logging
import os
#from env import ENDPOINT, ACCESS_ID, ACCESS_KEY, USERNAME, PASSWORD
from tuya_iot import (
    TuyaOpenAPI,
    AuthType,
    TuyaOpenMQ,
    TuyaDeviceManager,
    TuyaHomeManager,
    TuyaDeviceListener,
    TuyaDevice,
    TuyaTokenInfo,
    TUYA_LOGGER
)


TUYA_ENDPOINT = os.environ['TUYA_ENDPOINT']
TUYA_CLIENTID = os.environ['TUYA_CLIENTID']
TUYA_SECRET = os.environ['TUYA_SECRET']
TUYA_USERNAME = os.environ['TUYA_USERNAME']
TUYA_PASSWORD = os.environ['TUYA_PASSWORD']

DEVICE_ID = ""

TUYA_LOGGER.setLevel(logging.DEBUG)

print(TUYA_ENDPOINT,TUYA_CLIENTID,TUYA_SECRET,DEVICE_ID, TUYA_USERNAME, TUYA_PASSWORD)

def input_handler(command: str):
    print(f"Command entered: {command}")
    if command == "1":
        openapi = TuyaOpenAPI(TUYA_ENDPOINT,TUYA_CLIENTID,TUYA_SECRET)
        result = openapi.connect(TUYA_USERNAME,TUYA_PASSWORD,1,"tuyaSmart")
        #result = openapi.connect()
        #print(result)
        #location = openapi.get('/v1.0/iot-03/locations/ip?ip=your-ip-address')
        #print(location)
        result = openapi.get(f'/v1.0/iot-03/devices/{DEVICE_ID}/functions')
        print(result)

#GET: /v1.0/iot-03/devices/{device_id}/functions


while True:
    cmd = input('Enter command, q to quit: ')
    if cmd == "q": break
    input_handler(cmd)



# flag = not flag
# commands = {'commands': [{'code': 'switch_led', 'value': flag}]}
# openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)