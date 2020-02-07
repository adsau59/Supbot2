from supbot import Supbot


def process(supbot, request_command: str):
    parts = request_command.split(" ")
    try:
        if parts[0] == "quit":
            return supbot.quit()
        elif parts[0] == "send_message":
            return supbot.send_message(parts[1], parts[2])
        else:
            return "Invalid command"
    except IndexError:
        return "Insufficient Arguments"


def start_loop(supbot: Supbot):
    while supbot.is_on():
        request = input("?")
        response = process(supbot, request)
        print(response)


def print_message(contact, message):
    print(f"{contact}: {message}")


def main():
    with Supbot(message_received=print_message) as supbot:
        start_loop(supbot)


if __name__ == "__main__":
    main()
