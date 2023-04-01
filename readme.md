
# Light Controls
A Python program used to control [Tuya](https://www.tuya.com/) lights via the Tuya [IoT platform](https://iot.tuya.com/). I had Tuya-enabled lights installed on our porch because I wanted to be able to control the outdoor lights from an app and be able to change the light colors for different holidays. 

Each year our Halloween display has become progressively larger. I realized that I could programmatically control the lights via the Tuya IoT platform. The result is this project, a custom controller for light and audio sound effects for Halloween.

# Prereqs

## Configure a cloud project

To get this working initially, I first followed the Tuya
[Quick Start](https://developer.tuya.com/en/docs/iot/quick-start1?id=K95ztz9u9t89n) guide. I followed the `Smart Home` linking option - this allowed me to write code against the API but still maintain control via the Tuya Smart Home app.

## Configure a development environment

To get Python working, I followed the Tuya [Development environment](https://developer.tuya.com/en/docs/iot/device-control-best-practice-python?id=Kav4zc0nphsn5) guide.

The most confusing problems I had during intial setup were:

- The username & password you use for the Smart Home app are completely independent from the username & password you use for the Tuya IOT platform. They seem like they should be a single credential across both platforms, but that is not the case

- Connecting to the API as a Smart Home user. The country codes are documented [here](https://github.com/tuya/tuya-home-assistant/blob/main/docs/regions_dataCenters.md). I could not figure out the 4th required argument `Schema`. The helpfiles said it was a property of the application that you developed, but I didnt develop an application. I am just using the Tuya Smart Home app. I ended up opening a support ticket. Support pointed me to this [developer's document](https://developer.tuya.com/en/docs/iot/device-control-best-practice?id=Ka72202tz4m67) which led me to the proper schema.

    ```python
    openapi.connect(TUYA_USERNAME,TUYA_PASSWORD,1,"tuyaSmart")
    ```

## Environment Variables

5 environment variables are required. 
- `TUYA_ENDPOINT` is the URL corresponding to the location hosting your cloud project. A list of endpoint URLs can be found [here](https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4).
- `TUYA_CLIENTID` and `TUYA_SECRET` are found on the Overview tab of your cloud project.
- `TUYA_USERNAME` and `TUYA_PASSWORD` are the username and password you use to log into the Tuya IOT Developer Platform

## Devices 

Populate `devices.json` with key/value pairs, a friendly device name for the key and the device's Tuya ID for the value.
```json
{
    "MUSIC_ROOM": "ab1234567aa123a321abcd",
    "FRONT_DOOR": "cd3456789bb456b123bcde",
    "OFFICE": "ef4567890cc567c234cdef"
}
```

## Default device

If you want to play with the demo functions, set a default device ID in `input-monitor.py`. This is used by example functions that need a single device ID passed to it - the functions will use the default device ID.

```python
DEFAULT_DEVICE_ID = controller.device_dict["FRONT_DOOR"]
```

Linux
```bash
export TUYA_ENDPOINT="https://openapi.tuyaus.com"
export TUYA_CLIENTID="xxx"
export TUYA_SECRET="xxx"
export TUYA_USERNAME="user@domain.com"
export TUYA_PASSWORD="xxx"
```

Windows
```powershell
$env:TUYA_ENDPOINT='https://openapi.tuyaus.com'
$env:TUYA_CLIENTID='xxx'
$env:TUYA_SECRET='xxx'
$env:TUYA_USERNAME='user@domain.com'
$env:TUYA_PASSWORD='xxx'
```

# Usage

The idea behind this prorject is to have a Python program waiting for command line input to switch between scenes.

## Examples

`lightcontrols.py` contains classes designed to make it easier to interact with the Tuya API

`input-monitor.py` contains example functions demonstrating most of the functionality in `lightcontrols.py`



Linux/Mac
```bash
python3 input-monitor.py
```

Windows
```powershell
python ./input-monitor.py
```

Powering off the default device:

```powershell
PS C:\git\light-controls> python .\input-monitor.py
1 - Show device functions
2 - Turn device off
3 - Turn device on
4 - Flash
5 - Play sound
6 - Set HSV value
7 - Device status
8 - Device reset
9 - Tiptoe Through the Tulips flash
Enter command, x to exit: 2
Command entered: 2
{'result': True, 'success': True, 't': 1680380700899, 'tid': '471e7403d0cb11ed9c106a2c61a2ec08'}
1 - Show device functions
2 - Turn device off
3 - Turn device on
4 - Flash
5 - Play sound
6 - Set HSV value
7 - Device status
8 - Device reset
9 - TTT
Enter command, x to exit: x
PS C:\git\light-controls> 
