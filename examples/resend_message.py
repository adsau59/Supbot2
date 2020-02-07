from supbot import Supbot


def repeat_message(supbot, contact_name, message):
    supbot.send_message(contact_name, message)


with Supbot(message_received=repeat_message) as bot:
    bot.wait_for_finish()
