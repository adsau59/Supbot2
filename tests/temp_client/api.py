from tests.temp_client import network


def send_message(name: str, message: str):
    json_request = {"function": "run_action", "data": {"name": "send_message",
                                                       "params": {"chat": name, "message": message}}}
    return network.send_request(json_request)


def quit_supbot():
    return network.send_request({"function": "quit"})
