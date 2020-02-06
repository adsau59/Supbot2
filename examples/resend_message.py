import supbot


def repeat_message(contact_name, message):
    supbot.send_message(contact_name, message)


with supbot.EventHandler(message_received=repeat_message) as e:
    e.wait_for_finish()
