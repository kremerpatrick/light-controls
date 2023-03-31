import json
import logging
import os
import random
import sys
import time
from datetime import datetime, timedelta
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
            # Show device functions
            result = controller.openapi.get(f'/v1.0/iot-03/devices/{DEFAULT_DEVICE_ID}/functions')
            print(json.dumps(result,indent=4))

        case "2":
            # Turn device off
            result = controller.led_toggle(DEFAULT_DEVICE_ID,False)
            print(result)

        case "3":
            # Turn device on
            result = controller.led_toggle(DEFAULT_DEVICE_ID,True)
            print(result)

        case "4":
            # Flash sequence
            success = controller.led_toggle_all(False)
            success = controller.set_all_devices("white",1000,1000)

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

            except KeyboardInterrupt:
                print('Ctrl-C detected, exiting loop...')
                success = controller.led_toggle_all(True)
                success = controller.set_all_devices("white",1000,0)
            
            success = controller.led_toggle_all(True)
            success = controller.set_all_devices("white",1000,0)

        case "5":
            # Play a sound
            #playsound('mp3/thunder-crack-31702.mp3')
            #playsound('mp3/electricitysound001.mp3')
            #playsound('mp3/electricitysound002.mp3')
            filename = controller.get_random_sound(SoundCategory.ELECTRICITY)
            print(filename)
            playsound(filename)

        case "6":
            # Set a device HSV value
            result = controller.set_color_hsv(DEFAULT_DEVICE_ID,229,1000,1000)
            print(result)

        case "7":
            # Show device status
            result = controller.get_device_status(DEFAULT_DEVICE_ID)
            print(json.dumps(result,indent=4))

        case "8":
            # Reset all to white
            success = controller.led_toggle_all(False)
            success = controller.set_all_devices("white",1000,1000)
            # result = controller.set_work_mode(DEFAULT_DEVICE_ID,"white")
            # result = controller.set_bright_value_v2(DEFAULT_DEVICE_ID,1000)
            # result = controller.set_temp_value_v2(DEFAULT_DEVICE_ID,1000)
        
        case "9":
            # Tipoe Through the Tulips
            success = controller.led_toggle_all(True)
            #success = controller.set_all_devices("white",1000,1000)
            success = controller.set_all_devices("colour",1000,1000,34,1000,1000) #yellow
            controller.play_audio_thread('mp3/TttTandDemonicSquelching001.mp3')
            #playsound('mp3/TttTandDemonicSquelching001.mp3',block=False)
            time.sleep(15)
            success = controller.set_all_devices("colour",1000,1000,1,1000,1000) #red

            start_time = datetime.now()
            end_time = start_time + timedelta(seconds=49)

            cur_time = datetime.now()
            while end_time > cur_time:
                print(f'End {end_time}, cur {cur_time}')
                device_name = random.choice(list(controller.device_dict.keys()))
                result = controller.led_toggle(controller.device_dict[device_name],True)
                print(f'{device_name} set to powered on={False}, success={result["success"]}')
                result = controller.led_toggle(controller.device_dict[device_name],False)
                print(f'{device_name} set to powered on={True}, success={result["success"]}')
                cur_time = datetime.now()

            success = controller.led_toggle_all(False)
            

            

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
    print("9 - TTT")

while True:
    print_commands()
    cmd = input('Enter command, x to exit: ')
    if cmd == "x": break
    input_handler(cmd)



# flag = not flag
# commands = {'commands': [{'code': 'switch_led', 'value': flag}]}
# openapi.post('/v1.0/iot-03/devices/{}/commands'.format(DEVICE_ID), commands)