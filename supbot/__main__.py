"""
supbot

Usage:
  supbot [--device=<str>] [--no-server] [--port=<int>] [--no-prompt]
  supbot -h | --help
  supbot -v | --version

Options:
  -h --help         Show this screen.
  -v --version      Show version.
  --device=<str>    Device name
  --no-server       Doesn't run appium server
  --port=<int>      Port number to use to create/connect appium server
  --no-prompt       Don't use interactive console

"""
import re
import time

from prompt_toolkit import prompt
from prompt_toolkit.patch_stdout import patch_stdout

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


def start_loop(supbot: Supbot, no_prompt: bool):
    """
    Waits for input, then processes the input when entered
    loops till supbot is running

    :param no_prompt:
    :param supbot: supbot service
    """
    while not supbot.has_started():
        time.sleep(0.5)

    print(help_me)

    def get_input():
        with patch_stdout():
            while supbot.is_on():
                yield prompt("> ")

    while supbot.is_on():
        request = input("> ") if no_prompt else next(get_input())
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

    print("Loading...")

    with Supbot(message_received=print_message, no_server=args["--no-server"],
                port=args["--port"], device_name=args["--device"]) as supbot:
        start_loop(supbot, args["--no-prompt"])


if __name__ == "__main__":
    main()
