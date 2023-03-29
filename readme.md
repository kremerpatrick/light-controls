
# Light Controls
A Python program used to control [Tuya](https://www.tuya.com/) lights via the Tuya [IoT platform](https://iot.tuya.com/). I had Tuya-enabled lights installed on our porch because I wanted to be able to control the outdoor lights from an app and be able to change the light colors for different holidays. 

Each year our Halloween display has become progressively larger. I realized that I could programmatically control the lights via the Tuya IoT platform. The result is this project, a custom controller for light and audio sound effects for Halloween.

# Prereqs

## Configure a cloud project

To get this working initially, I first followed the Tuya
[Quick Start](https://developer.tuya.com/en/docs/iot/quick-start1?id=K95ztz9u9t89n) guide. I followed the `Smart Home` linking option - this allowed me to write code against the API but still maintain control via the Tuya Smart Home app.

To get Python working, I followed the Tuya [Development environment](https://developer.tuya.com/en/docs/iot/device-control-best-practice-python?id=Kav4zc0nphsn5) guide.

The most confusing problems I had during intial setup were:

- The username & password you use for the Smart Home app are completely independent from the username & password you use for the Tuya IOT platform. They seem like they should be a single credential across both platforms, but that is not the case

- Connecting to the API as a Smart Home user. The country codes are documented [here](https://github.com/tuya/tuya-home-assistant/blob/main/docs/regions_dataCenters.md). I could not figure out the 4th required argument `Schema`. The helpfiles said it was a property of the application that you developed - but I didnt develop an application in Smart Home mode. I ended up opening a support ticket. Support pointed me to this [developer's document](https://developer.tuya.com/en/docs/iot/device-control-best-practice?id=Ka72202tz4m67) which led me to the proper schema.

    ```python
    openapi.connect(TUYA_USERNAME,TUYA_PASSWORD,1,"tuyaSmart")
    ```

## Environment Variables

5 environment variables are required. 
- `TUYA_ENDPOINT` is the URL corresponding to the location hosting your cloud project. A list of endpoint URLs can be found [here](https://developer.tuya.com/en/docs/iot/api-request?id=Ka4a8uuo1j4t4).
- `TUYA_CLIENTID` and `TUYA_SECRET` are found on the Overview tab of your cloud project.
- `TUYA_USERNAME` and `TUYA_PASSWORD` are the username and password you use to log into the Tuya IOT Developer Platform

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