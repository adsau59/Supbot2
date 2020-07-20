"""
Simple example which resends messages sent to the bot
"""

from supbot import Supbot


def action_complete_callback(success, action_id, action):
    action_name, data = action

    msg = "successful" if success else "unsuccess"
    print(f"action {action_id} was {msg}")


def repeat_message(contact_name, message):
    """
    Supbot callbacks returns a reference for supbot's interface too
    :param contact_name:
    :param message:
    :return:
    """
    action_id = supbot.send_message(contact_name, message)
    print(f"sent action request: {action_id}")


"""
Supbot requires to initialize before you can use its services, so it should never be used out of its scope,
you can use with-as statement in order to automatically initialize supbot.
After it is created, you can use its services within its block.
"""
with Supbot(message_received=repeat_message, action_complete_callback=action_complete_callback) as supbot:
    supbot.wait_for_finish()
