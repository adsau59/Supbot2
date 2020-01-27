from tests.temp_client import api


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
