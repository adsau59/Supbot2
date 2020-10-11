from supbot import Supbot
from supbot.action import Action

contact = "123456789"


def action_callback(action: Action):
    print(action)


with Supbot() as supbot:
    supbot.send_message(contact, "hi", action_callback)
    supbot.quit()
