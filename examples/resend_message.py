"""
Simple example which resends messages sent to the bot
"""

from supbot import Supbot


def repeat_message(contact_name, message):
    """
    sends back the message received
    """
    action_id = supbot.send_message(contact_name, message)
    print(f"sent action request: {action_id}")
    success = supbot.wait_for_action(action_id)

    success_msg = "successful" if success else "unsuccessful"
    print(f"action {action_id}, sending '{message}' to {contact_name} was {success_msg}")


"""
Supbot requires to initialize before you can use its services, so it should never be used out of its scope,
you can use with-as statement in order to automatically initialize supbot.
After it is created, you can use its services within its block.
"""
with Supbot(message_received=repeat_message) as supbot:
    supbot.wait_for_finish()
