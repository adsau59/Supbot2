"""
Simple example which resends messages sent to the bot
"""

from supbot import Supbot
from supbot.action import ActionName


def action_complete_callback(success, action_id, action):
    """
    called when action is completed
    :param success: if the action was successfully called or not
    :param action_id: id of the action
    :param action: name and data of the action
    """
    action_name, data = action

    if action_id == ActionName.SEND_MESSAGE:
        contact, message = data
        success_msg = "successful" if success else "unsuccessful"
        print(f"action {action_id}, sending '{message}' to {contact} was {success_msg}")


def repeat_message(contact_name, message):
    """
    sends back the message received
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
