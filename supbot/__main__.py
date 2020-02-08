"""
Sample application of supbot which takes in commands to run actions,
and prints incoming events on screen
made just to test the library
"""

from supbot import Supbot


def process(supbot: Supbot, request_command: str):
    """
    reads request command string and performs appropriate function
    return response to print

    :param supbot: supbot service
    :param request_command: request string
    :return:
    """
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
    """
    Waits for input, then processes the input when entered
    loops till supbot is running

    :param supbot: supbot service
    """
    while supbot.is_on():
        request = input("?")
        response = process(supbot, request)
        print(response)


def print_message(supbot, contact, message):
    """
    callback method for message received event

    :param contact: name of the contact
    :param message: message string
    """
    print(f"{contact}: {message}")


def main():
    """
    starts the bot then waits for input
    """
    with Supbot(message_received=print_message) as supbot:
        start_loop(supbot)


if __name__ == "__main__":
    main()
