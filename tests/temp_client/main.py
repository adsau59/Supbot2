import threading
from dataclasses import dataclass

from tests.temp_client import network
from tests.temp_client.command_parser import process


@dataclass
class System:
    is_on = True


def main():
    system = System()

    event_server = threading.Thread(target=network.receive_event, args=(system,))
    event_server.start()

    while system.is_on:
        request = input("?")
        response = process(request)

        if request == "quit":
            system.is_on = False

        print(response)

    event_server.join()


if __name__ == "__main__":
    main()
