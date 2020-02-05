import supbot


def repeat_message(contact_name, messages):
    for m in messages:
        supbot.send_message(contact_name, m)


with supbot.EventHandler(message_received=repeat_message) as e:
    e.wait_for_finish()
