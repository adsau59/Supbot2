# Supbot2
[![Discord Chat](https://img.shields.io/discord/430649963597266945.svg)](https://discordapp.com/invite/V6e2fpc) 
[![Donations Badge](https://yourdonation.rocks/images/badge.svg)]({https://www.paypal.me/AdamSaudagar})
[![GitHub stars](https://img.shields.io/github/stars/adsau59/supbot2.svg?style=social&label=Star&maxAge=2592000)](https://github.com/adsau59/supbot2/stargazers/)

<div align="center">
  <img src="https://cdn.steemitimages.com/DQmVfVL98g7QbEyb4t4bt5A9DuMZLBYpiekwceBswjSUqTJ/small%20banner.jpg"/>
</div>

## Table of Contents
* [About the Project](#about-the-project)
  * [Requirements](#requirements)
  * [Technology Stack](#technology-stack)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
  * [Usage](#usage)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)

## About The Project

Supbot2 is an unofficial WhatsApp automation library written in Python which can be used to create bots. Supbot2 uses Appium to automate WhatsApp application to read the GUI and call respective events, and perform various actions on the GUI.

[Supbot API (1.0)](https://github.com/adsau59/supbot) was extremely tedious to setup and even more difficult to use. Not only that it required to have a phone and Supbot server connected to the Internet, which made it very unstable and unreliable. Supbot2 tries to fix these issues.

### Objective
- To create an easy to use way of automating WhatsApp App.
- To make a fail safe foundation for the developers to create their business logic without worrying about the stability and reliability of the application.

### Requirements
- Android phone/emulator
- A phone number to setup WhatsApp
- PC to run the Server

### Technology Stack
Supbot2 is made using
- [Python 3.7.1](https://www.python.org/downloads/release/python-371/)
- [Appium](http://appium.io/downloads.html)

## Getting started

### Prerequisites
You will need to setup Appium and Whatsapp before you start with Supbot
- Download and install [JDK](https://www.oracle.com/technetwork/java/javase/downloads/index.html), [Android SDK](https://developer.android.com/studio/releases/sdk-tools), [Appium](http://appium.io/downloads.html)
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

### Installation
For now there is no installable package for Supbot2, so just
- Download/Clone the repository from [github](https://github.com/adsau59/supbot2).
- Create a python file in the parent directory of supbot package and use `import supbot` to use the library.

### Usage
Following code resends the message received from (in just 5 LOC!)
```python
from supbot import Supbot


def repeat_message(supbot, contact_name, message):
    supbot.send_message(contact_name, message)


with Supbot(message_received=repeat_message) as bot:
    bot.wait_for_finish()
```

## Roadmap
Check out the [Trello](https://trello.com/b/aNlbWMEM/supbot2) board, to see what I'm working on and whats next.

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **extremely appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License
Distributed under the MIT License. See [LICENSE](https://github.com/adsau59/Supbot2/blob/master/LICENSE) for more information.

## Contact
If you have any problems or you want to contact me for feature ideas or want to collaborate in development you can contact me on [DefineX Community discord server](https://discord.gg/V6e2fpc).