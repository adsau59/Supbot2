# Supbot2

Unoffical WhatsApp Automation Library for Python

---

<div align="center">
  <img src="https://cdn.steemitimages.com/DQmVfVL98g7QbEyb4t4bt5A9DuMZLBYpiekwceBswjSUqTJ/small%20banner.jpg"/>
</div>

## Overview
Supbot2 is an unofficial WhatsApp automation library written in Python which can be used to create bots. Supbot2 uses Appium to automate WhatsApp application to read the GUI and call respective events, and perform various actions on the GUI.

[Supbot API (1.0)](https://github.com/adsau59/supbot) was extremely tedious to setup and even more difficult to use. Not only that it required to have a phone and Supbot server connected to the Internet, which made it very unstable and unreliable. Supbot2 tries to fix these issues.

### Easy to Use

Supbot is exeremly easy and intuitive to use library. It's API is made of just two types of services: `Action` and `Events`, which are basically simple function calls.

### Aims for Stability

Supbot aims for developers to just concentrate on building the business logic, and not to worry about how the library works. We want the API work flawlessly.

---

## Installation

### Requirements
- Android phone/emulator
- A phone number to setup WhatsApp
- PC

### Installing Appium
You will need to setup Appium and Whatsapp before you start with Supbot

- Download and install [JDK](https://www.oracle.com/technetwork/java/javase/downloads/index.html), [Android SDK](https://developer.android.com/studio/releases/sdk-tools), and [Appium](http://appium.io/downloads.html)
- Create %JAVA_HOME% and %ANDROID_HOME% environment variables
- Connect your phone via usb, and start debuging 
- -OR- Create an android emulator
- Install WhatsApp and set it up to reach on the main chat screen.
- Get `deviceName` of your android device by using `adb devices` command.
- Run appium server and try running this configuration with the `deviceName` of your device.
```
{
"appPackage": "com.whatsapp",
"deviceName": "",
"platformName": "android",
"noReset": "true",
"appActivity": "com.whatsapp.HomeActivity"
}
```
If the whatsapp app opens up in your device automatically, Appium is setup perfectly

### Installing Supbot
You will need Python >=3.6 in order to install supbot. Supbot is developed using [Python 3.7.1](https://www.python.org/downloads/release/python-371/), so its recomended to use that, so that you don't encouter unexpected issues.  
<br/>
Install the `supbot` package using
```
pip install supbot
```
---

## Getting Started
Following code resends the message received from a contact (in just 5 LOC!).  
Visit [Overview](how-to-use/overview.md) to understand the code.
```python
from supbot import Supbot


def repeat_message(contact_name, message):
    supbot.send_message(contact_name, message)


with Supbot(message_received=repeat_message) as supbot:
    supbot.wait_for_finish()
```

## Roadmap
Check out the [Trello](https://trello.com/b/aNlbWMEM/supbot2) board, to see what I'm working on and whats next.

## License
Distributed under the MIT License. See [LICENSE](https://github.com/adsau59/Supbot2/blob/master/LICENSE) for more information.

## Contact
If you have any problems or you want to contact me for feature ideas or want to collaborate in development you can contact me on [DefineX Community discord server](https://discord.gg/V6e2fpc).