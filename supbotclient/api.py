import threading
from typing import List, Callable
from supbotclient import network


class EventHandler:

    def __init__(self, message_received: Callable[[str, List[str]], None] = None):
        self.message_received = message_received
        self.is_on = True
        self.event_server = threading.Thread(target=network.receive_event, args=(self,))

    def start(self):
        self.event_server.start()

    def wait_for_finish(self):
        self.event_server.join()

    def call_event(self, name: str, params: dict):
        if name == "new_message" and self.message_received is not None:
            self.message_received(params["chat_name"], params["messages"])

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def send_message(name: str, message: str):
    json_request = {"function": "run_action", "data": {"name": "send_message",
                                                       "params": {"chat": name, "message": message}}}
    return network.send_request(json_request)


def quit_supbot():
    return network.send_request({"function": "quit"})
