import json
import logging
import os
import random
import sys
import time
from playsound import playsound
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
from lightcontrols import LightControls,SoundCategory

MIN_PYTHON = (3,10,7)
assert sys.version_info >= MIN_PYTHON, f"Python {'.'.join([str(n) for n in MIN_PYTHON])} or newer is required."

try:
    TUYA_ENDPOINT = os.environ['TUYA_ENDPOINT']
    TUYA_CLIENTID = os.environ['TUYA_CLIENTID']
    TUYA_SECRET = os.environ['TUYA_SECRET']
    TUYA_USERNAME = os.environ['TUYA_USERNAME']
    TUYA_PASSWORD = os.environ['TUYA_PASSWORD']
except KeyError as e:
    print(f'Missing environment variable: {e}')
    sys.exit()

#TUYA_LOGGER.setLevel(logging.DEBUG)
controller = LightControls(TUYA_ENDPOINT, TUYA_CLIENTID, TUYA_SECRET, TUYA_USERNAME, TUYA_PASSWORD)

success = controller.load_devices()
if not success:
    print("Ending program, unable to load device list.")
    sys.exit()

DEFAULT_DEVICE_ID = controller.device_dict["FRONT_DOOR"]

def input_handler(command: str):
    print(f"Command entered: {command}")

    match command:
        case "1":
            result = controller.openapi.get(f'/v1.0/iot-03/devices/{DEFAULT_DEVICE_ID}/functions')
            print(json.dumps(result,indent=4))

        case "2":
            result = controller.led_toggle(DEFAULT_DEVICE_ID,False)
            print(result)

        case "3":
            result = controller.led_toggle(DEFAULT_DEVICE_ID,True)
            print(result)

        case "4":

            try:
                MAX_LOOP = 3000
                for i in range(1,MAX_LOOP):
                    print(f'Running flash loop. {i}/{MAX_LOOP} Press ^C to exit the loop.')
                    device_name = random.choice(list(controller.device_dict.keys()))
                    result = controller.led_toggle(controller.device_dict[device_name],True)
                    print(f'{device_name} set to powered on={False}, success={result["success"]}')
                    playsound(controller.get_random_sound(SoundCategory.ELECTRICITY))
                    result = controller.led_toggle(controller.device_dict[device_name],False)
                    print(f'{device_name} set to powered on={True}, success={result["success"]}')

                    # result = controller.led_toggle(device_dict["CORNER"],powered_on)
                    # print(f'CORNER set to powered on={powered_on}, success={result["success"]}')
                    # playsound(controller.get_random_sound(SoundCategory.ELECTRICITY))

                    # result = controller.led_toggle(device_dict["FRONT_DOOR"],powered_on)
                    # print(f'FRONT_DOOR set to powered on={powered_on}, success={result["success"]}')
                    # playsound(controller.get_random_sound(SoundCategory.ELECTRICITY))

                    # result = controller.led_toggle(device_dict["OFFICE"],powered_on)
                    # print(f'OFFICE set to powered on={powered_on}, success={result["success"]}')
                    # playsound(controller.get_random_sound(SoundCategory.ELECTRICITY))

                    # result = controller.led_toggle(device_dict["MUSIC_ROOM"],powered_on)
                    # print(f'MUSIC_ROOM set to powered on={powered_on}, success={result["success"]}')
                    # playsound(controller.get_random_sound(SoundCategory.ELECTRICITY))
            except KeyboardInterrupt:
                print('Ctrl-C detected, exiting loop...')

        case "5":
            #playsound('mp3/thunder-crack-31702.mp3')
            #playsound('mp3/electricitysound001.mp3')
            #playsound('mp3/electricitysound002.mp3')
            filename = controller.get_random_sound(SoundCategory.ELECTRICITY)
            print(filename)
            playsound(filename)

        case "6":
            result = controller.set_color_hsv(DEFAULT_DEVICE_ID,229,1000,1000)
            print(result)

        case "7":
            result = controller.get_device_status(DEFAULT_DEVICE_ID)
            print(json.dumps(result,indent=4))

        case "8":
            result = controller.set_work_mode(DEFAULT_DEVICE_ID,"white")
            result = controller.set_bright_value_v2(DEFAULT_DEVICE_ID,1000)
            result = controller.set_temp_value_v2(DEFAULT_DEVICE_ID,1000)

#GET: /v1.0/iot-03/devices/{device_id}/functions

def print_commands():
    print("1 - Show device functions")
    print("2 - Turn device off")
    print("3 - Turn device on")
    print("4 - Flash")
    print("5 - Play sound")
    print("6 - Set HSV value")
    print("7 - Device status")
    print("8 - Device reset")

while True:
    print_commands()
    cmd = input('Enter command, x to exit: ')
    if cmd == "x": break
    input_handler(cmd)



# flag = not flag
# commands = {'commands': [{'code': 'switch_led', 'value': flag}]}
# openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)