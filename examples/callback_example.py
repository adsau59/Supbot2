from supbot import Supbot

contact = "123456789"


def action_callback_with_param(action_id):
    action = supbot.get_action(action_id)
    print(action)


with Supbot() as supbot:
    supbot.send_message(contact, "hi", action_callback_with_param)
    supbot.quit()
