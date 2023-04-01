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

def input_handler(command: str):
    print(f"Command entered: {command}")

    match command:
        case "1":
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

        case "2":
            # Tiptoe through the Tulips
            # Start with yellow lighting
            success = controller.led_toggle_all(True)
            success = controller.set_all_devices("colour",1000,1000,34,1000,1000) #yellow

            # Begin the song, wait for the 15 second mark, the demonic sounds start at that mark, flip lights to red
            controller.play_audio_thread('mp3/TttTandDemonicSquelching001.mp3')
            time.sleep(15)
            success = controller.set_all_devices("colour",1000,1000,1,1000,1000) #red

            # Sound lasts for another 49 seconds
            start_time = datetime.now()
            end_time = start_time + timedelta(seconds=49)

            # Blink a random light for the rest of the song
            cur_time = datetime.now()
            while end_time > cur_time:
                print(f'End {end_time}, cur {cur_time}')
                device_name = random.choice(list(controller.device_dict.keys()))
                result = controller.led_toggle(controller.device_dict[device_name],True)
                print(f'{device_name} set to powered on={False}, success={result["success"]}')
                result = controller.led_toggle(controller.device_dict[device_name],False)
                print(f'{device_name} set to powered on={True}, success={result["success"]}')
                cur_time = datetime.now()

            # Lights out at the end
            success = controller.led_toggle_all(False)


def print_commands():
    print("1 - Flash")
    print("2 - Tiptoe Through the Tulips Flash")

while True:
    print_commands()
    cmd = input('Enter command, x to exit: ')
    if cmd == "x": break
    input_handler(cmd)