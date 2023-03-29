import json
import logging
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

TUYA_LOGGER.setLevel(logging.DEBUG)

class LightControls:

    def __init__(self, TUYA_ENDPOINT: str, TUYA_CLIENTID: str, TUYA_SECRET: str, TUYA_USERNAME: str, TUYA_PASSWORD: str):
        self.TUYA_ENDPOINT = TUYA_ENDPOINT
        self.TUYA_CLIENTID = TUYA_CLIENTID
        self.TUYA_SECRET = TUYA_SECRET
        self.TUYA_USERNAME = TUYA_USERNAME
        self.TUYA_PASSWORD = TUYA_PASSWORD

        self.openapi = TuyaOpenAPI(TUYA_ENDPOINT,TUYA_CLIENTID,TUYA_SECRET)
        result = self.openapi.connect(TUYA_USERNAME,TUYA_PASSWORD,1,"tuyaSmart")

    def led_toggle(self,deviceid: str, led_on: bool):
            commands = {'commands': [{'code': 'switch_led', 'value': led_on}]}
            result = self.openapi.post(f'/v1.0/iot-03/devices/{deviceid}/commands', commands)
            return result
