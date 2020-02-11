# Supbot2 
[![Discord Chat](https://img.shields.io/discord/430649963597266945.svg)](https://discordapp.com/invite/V6e2fpc) [![Donations Badge](https://yourdonation.rocks/images/badge.svg)](https://www.paypal.me/AdamSaudagar) [![GitHub stars](https://img.shields.io/github/stars/adsau59/supbot2.svg?style=social&label=Star&maxAge=2592000)](https://github.com/adsau59/supbot2/stargazers/)

Simplest WhatsApp automation Library for Python

---

Supbot2 is an unofficial WhatsApp automation library written in Python which can be used to create bots. Supbot2 uses Appium to automate WhatsApp application on your android device/emulator, and perform various actions (like sending message), and also trigger events (like receiving message).

- Learn how to install, visit [Supbot2 Documentation](https://adsau59.github.io/Supbot2/index.html)
- Chat with us on [Discord](http://discord.definex.in)

## Usage
Following code resends the message received from a contact (in just 5 LOC!).  
```python
from supbot import Supbot


def repeat_message(contact_name, message):
    supbot.send_message(contact_name, message)


with Supbot(message_received=repeat_message) as supbot:
    supbot.wait_for_finish()
```