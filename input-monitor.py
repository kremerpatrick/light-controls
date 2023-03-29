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

#TUYA_LOGGER.setLevel(logging.DEBUG)

#print(TUYA_ENDPOINT,TUYA_CLIENTID,TUYA_SECRET,DEVICE_ID, TUYA_USERNAME, TUYA_PASSWORD)

def input_handler(command: str):
    print(f"Command entered: {command}")
    openapi = TuyaOpenAPI(TUYA_ENDPOINT,TUYA_CLIENTID,TUYA_SECRET)
    result = openapi.connect(TUYA_USERNAME,TUYA_PASSWORD,1,"tuyaSmart")

    match command:
        case "1":
            #result = openapi.connect()
            #print(result)
            #location = openapi.get('/v1.0/iot-03/locations/ip?ip=your-ip-address')
            #print(location)
            result = openapi.get(f'/v1.0/iot-03/devices/{DEVICE_ID}/functions')
            print(json.dumps(result,indent=4))

        case "2":
            commands = {'commands': [{'code': 'switch_led', 'value': False}]}
            result = openapi.post(f'/v1.0/iot-03/devices/{DEVICE_ID}/commands', commands)

        case "3":
            commands = {'commands': [{'code': 'switch_led', 'value': True}]}
            result = openapi.post(f'/v1.0/iot-03/devices/{DEVICE_ID}/commands', commands)


#GET: /v1.0/iot-03/devices/{device_id}/functions

def print_commands():
    print("1 - Show device functions")
    print("2 - Turn device off")
    print("3 - Turn device on")

while True:
    print_commands()
    cmd = input('Enter command, q to quit: ')
    if cmd == "q": break
    input_handler(cmd)



# flag = not flag
# commands = {'commands': [{'code': 'switch_led', 'value': flag}]}
# openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)