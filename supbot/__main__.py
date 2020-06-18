"""
supbot

Usage:
  supbot [--device=<str>]
  supbot -h | --help
  supbot -v | --version

Options:
  -h --help         Show this screen.
  -v --version         Show version.
  --device=<str>    Device name

"""
import re
import time

from supbot import Supbot
from docopt import docopt

help_me = """Available commands:
send <contact-name> <message>
quit"""


def process(supbot: Supbot, request_command: str):
    """
    reads request command string and performs appropriate function
    return response to print

    :param supbot: supbot service
    :param request_command: request string
    :return:
    """
    match = re.findall(r"([^\s\"']+|\"([^\"]*)\"|'([^']*)')", request_command)
    parts = [x[0] if x[1] == "" else x[1] for x in match]
    try:
        if parts[0] == "quit":
            supbot.quit()
        elif parts[0] == "send":
            supbot.send_message(parts[1], parts[2])
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
    while not supbot.has_started():
        time.sleep(0.5)

    print(help_me)

    while supbot.is_on():
        request = input(">")
        process(supbot, request)


def print_message(contact, message):
    """
    callback method for message received event

    :param _: supbot object, not useful in this instance
    :param contact: name of the contact
    :param message: message string
    """
    print(f"{contact}: {message}")


def main():
    """
    Sample application of supbot which takes in commands to run actions,
    and prints incoming events on screen
    made just to tests the library

    starts the bot then waits for input
    """
    args = docopt(__doc__)

    if args["--version"]:
        from supbot import __version__
        print("supbot v{}".format(__version__))
        return

    device_name = args["--device"]

    print("Loading...")

    with Supbot(device_name=device_name, message_received=print_message) as supbot:
        start_loop(supbot)


if __name__ == "__main__":
    main()
