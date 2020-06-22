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

### Creating Environment
You will need to setup Appium and Whatsapp before you start with Supbot

- Download and install [JDK](https://www.oracle.com/in/java/technologies/javase/javase-jdk8-downloads.html), [Android Studio](https://developer.android.com/studio), and [NPM](https://nodejs.org/en/)
- Create `JAVA_HOME` environment variable by default it is `C:\PROGRA~1\Java\jdk1.8.0_181` in windows (don't forget to change the jdk version depending on what version you have installed)
- Create `ANDROID_HOME` environment variable by default it is `%USERPROFILE%\AppData\Local\Android\Sdk`in windows
- Install Appium using `npm install -g appium`
- Connect your phone via usb, and start debugging 
- -OR- Create and run android emulator using AVD manager
- Install WhatsApp and set it up to reach on the main chat screen.
- (Optional) Create an empty whatsapp group named `!temp` (You can do this by adding 1 contact to the group then kicking them out)

### Installing Supbot
You will need Python >=3.6 in order to install supbot. Supbot is developed using [Python 3.7.1](https://www.python.org/downloads/release/python-371/), so its recomended to use that, so that you don't encouter unexpected issues.  
<br/>
Install the `supbot` package using
```
pip install supbot
```
You can test supbot by running `supbot` in terminal / powershell, and use the given commands to run some test functions

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