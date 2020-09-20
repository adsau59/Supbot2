"""
Simple example which resends messages sent to the bot
"""

from supbot import Supbot


def repeat_message(group_name, contact, message):
    """
    sends back the message received
    """
    # sending personal message
    supbot.send_message(contact, f"You sent {message} to {group_name}")

    # sending message in group
    supbot.send_message(group_name, message)


"""
Supbot requires to initialize before you can use its services, so it should never be used out of its scope,
you can use with-as statement in order to automatically initialize supbot.
After it is created, you can use its services within its block.
"""
with Supbot(group_message_received=repeat_message) as supbot:
    supbot.wait_for_finish()
