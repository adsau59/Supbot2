from supbotclient import api, EventHandler


def process(request_command: str):
    parts = request_command.split(" ")
    try:
        if parts[0] == "quit":
            return api.quit_supbot()
        elif parts[0] == "send_message":
            return api.send_message(parts[1], parts[2])
        else:
            return "Invalid command"
    except IndexError:
        return "Insufficient Arguments"


def start_loop(event: EventHandler):
    while event.is_on:
        request = input("?")
        response = process(request)

        if request == "quit":
            event.is_on = False

        print(response)


def print_message(contact, message):
    print(f"{contact}: {message}")


if __name__ == "__main__":
    with api.EventHandler(message_received=print_message) as e:
        start_loop(e)
        e.wait_for_finish()
