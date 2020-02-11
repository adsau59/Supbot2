"""
Simple example which resends messages sent to the bot
"""

from supbot import Supbot


def repeat_message(contact_name, message):
    """
    Supbot callbacks returns a reference for supbot's interface too
    :param contact_name:
    :param message:
    :return:
    """
    supbot.send_message(contact_name, message)


"""
Supbot requires to initialize before you can use its services, so it should never be used out of its scope,
you can use with-as statement in order to automatically initialize supbot.
After it is created, you can use its services within its block.
"""
with Supbot(message_received=repeat_message) as supbot:
    supbot.wait_for_finish()
