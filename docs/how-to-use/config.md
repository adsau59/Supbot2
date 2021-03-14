# Configuration

List of configuration accepted by Supbot

---

Supbot2 can be configured using Parameters which is passed into the constructor while creating supbot object.

#### Example
```python
with Supbot(device="abcd") as supbot:
```
over here `device` parameter is set to "abcd". Configuration can also be used when running supbot though CLI using arguments. 

Table given below represents the list of paramters and what it does.

| Parameter           | CLI Argument            | Description                                                                                                                                                               | Parameter Example             | CLI Example                  |
|---------------------|-------------------------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------|------------------------------|
| device, device_name | --device, --device-name | Specify the android device to use instead of searching automatically using adb                                                                                            | Supbot(device="emulator1234") | supbot --device emulator1234 |
| no_server           | --no-server             | Don't run appium server inside supbot, used when hosting appium server separately                                                                                         | Supbot(no_server=True)        | supbot --no-server           |
| port                | --port                  | Specify the port to host/connect appium server using, when not specified, use any random unused port, if hosting appium server inside supbot.                             | Supbot(port=12345)            | supbot --port=12345          |
| check_wait          | --check-wait            | Default: 5, specify the seconds to wait for checking UI in critical situations. Use larger value for slow devices, but increasing it might degrade performance of supbot. | Supbot(check_wait=10)         | supbot --check-wait 10       |
| -                   | --no-prompt             | Don't use interactive console                                                                                                                                             | -                             | supbot --no-prompt           |
| verbose             | --verbose               | Enable verbose mode for debug logs in console, and appium logs in appium.log file                                                                                                                                             | -                             | supbot --no-prompt           |
