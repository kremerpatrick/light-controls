import glob
import json
import logging
import random

from enum import Enum
from playsound import playsound
from threading import Thread
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

#TUYA_LOGGER.setLevel(logging.DEBUG)

class SoundCategory(Enum):
    """Available sound categories"""

    ELECTRICITY = 0
    THUNDER = 1

class LightControls:
    """A class to simplfy interacting with the Tuya REST API"""
    def __init__(self, TUYA_ENDPOINT: str, TUYA_CLIENTID: str, TUYA_SECRET: str, TUYA_USERNAME: str, TUYA_PASSWORD: str):
        self.TUYA_ENDPOINT = TUYA_ENDPOINT
        self.TUYA_CLIENTID = TUYA_CLIENTID
        self.TUYA_SECRET = TUYA_SECRET
        self.TUYA_USERNAME = TUYA_USERNAME
        self.TUYA_PASSWORD = TUYA_PASSWORD
        
        self.device_dict = {}

        self.openapi = TuyaOpenAPI(TUYA_ENDPOINT,TUYA_CLIENTID,TUYA_SECRET)
        result = self.openapi.connect(TUYA_USERNAME,TUYA_PASSWORD,1,"tuyaSmart")
        if result["success"] is False:
            raise Exception(f"Connection failed with error code: {result['code']}, description: {result['msg']}")

    def get_device_status(self, deviceid: str):
        """Returns device status"""
        result = self.openapi.get(f'/v1.0/iot-03/devices/{deviceid}/status')
        return result

    def led_toggle_all(self, led_on: bool):
        """Toggle LED status for all devices on or off"""

        all_success = True
        for deviceid in self.device_dict.values():
            result = self.led_toggle(deviceid,led_on)
            if result["success"] == False:
                print(result)
                all_success = False
        return all_success

    def set_all_devices(self, work_mode: str, bright_value: int, temp_value: int, hue: int = None, saturation: int = None, value: int = None):
        """Set all devices to specified values"""

        all_success = True
        if work_mode == "colour" and (hue is None or saturation is None or value is None):
            all_success = False
            print('Hue, saturation, and value are required if work_mode is set to colour')
            return all_success

        for deviceid in self.device_dict.values():
            result = self.set_work_mode(deviceid,work_mode)
            if result["success"] == False:
                print(result)
                all_success = False

            result = self.set_bright_value_v2(deviceid,bright_value)
            if result["success"] == False:
                print(result)
                all_success = False

            result = self.set_temp_value_v2(deviceid,temp_value)
            if result["success"] == False:
                print(result)
                all_success = False
            
            if work_mode == "colour":
                result = self.set_color_hsv(deviceid,hue,saturation,value)
                if result["success"] == False:
                    print(result)
                    all_success = False

        return all_success


    def led_toggle(self,deviceid: str, led_on: bool):
        """Set a device LED status on or off"""
        commands = {'commands': [{'code': 'switch_led', 'value': led_on}]}
        result = self.openapi.post(f'/v1.0/iot-03/devices/{deviceid}/commands', commands)
        return result

    def load_devices(self,device_filename='devices.json'):
        try:
            with open(device_filename,'r') as file:
                self.device_dict = json.load(file)
                return True
        except Exception as e:
            print(f'Cound not retrieve devices list: {e}')
            return False

    def play_audio_thread(self,filepath: str):
        """Play audio file in a non-blocking thread"""
        # https://stackoverflow.com/questions/44472162/how-can-i-play-audio-playsound-in-the-background-of-a-python-script
        # I tried using the block=False option in playsound but it won't work on Windows because of this bug:
        #  https://github.com/TaylorSMarks/playsound/issues/102

        def play_thread_function():
            playsound(filepath)

        play_thread = Thread(target=play_thread_function)
        play_thread.start()

    def set_color_hsv(self, deviceid: str, hue: int, saturation: int, value: int):
        """Sets a devices color with HSV (Hue, Saturation, Value)"""
        commands = {
                    "commands":[
                        {
                            "code":"colour_data_v2",
                            "value":{
                                "h":hue,
                                "s":saturation,
                                "v":value
                                }
                        }
                    ]
                }
        result = self.openapi.post(f'/v1.0/iot-03/devices/{deviceid}/commands', commands)
        return result

    def set_bright_value_v2(self, deviceid: str, bright_value: int):
        """Sets a device brighness"""
        commands = {
            "commands":[
                {
                    "code":"bright_value_v2",
                    "value": bright_value
                }
            ]
        }
        result = self.openapi.post(f'/v1.0/iot-03/devices/{deviceid}/commands', commands)
        return result

    def set_temp_value_v2(self, deviceid: str, temp_value: int):
        """Sets a device temperature"""
        commands = {
            "commands":[
                {
                    "code":"temp_value_v2",
                    "value": temp_value
                }
            ]
        }
        result = self.openapi.post(f'/v1.0/iot-03/devices/{deviceid}/commands', commands)
        return result

    def set_work_mode(self, deviceid: str, work_mode: str):
        """Sets a device work mode (white, colour, scene, music"""
        commands = {
            "commands":[
                {
                    "code":"work_mode",
                    "value": work_mode
                }
            ]
        }
        result = self.openapi.post(f'/v1.0/iot-03/devices/{deviceid}/commands', commands)
        return result

    def get_random_sound(self,sound_category: SoundCategory):
        """Select a random audio file in the /mp3 folder based on category"""
        match sound_category:
            case SoundCategory.ELECTRICITY:
                fnames = 'mp3/electricitysound*.mp3'
            
            case SoundCategory.THUNDER:
                fnames = 'mp3/thundersound*.mp3'
                
        filelist = glob.glob(fnames)
        num_files = len(filelist)
        random_file = random.randrange(num_files)
        return filelist[random_file]