import threading
from abc import ABC, abstractmethod
from typing import List, Callable, Tuple

import loguru
from typeguard import check_type

from supbot import looper
from supbot.model import Action, Event, ActionBuffer, ActionName
from supbot.system import System

_action_buffer: ActionBuffer = []
_system = System(loguru.logger)


class IEventHandler(ABC):

    @abstractmethod
    def call_event(self, event: Event, params: Tuple):
        pass


class EventHandler(IEventHandler):

    def __init__(self, message_received: Callable[[str, List[str]], None] = None):
        self.looper_thread = threading.Thread(target=looper.start, args=(_action_buffer, self, _system,))
        self.message_received = message_received

    def wait_for_finish(self):
        self.looper_thread.join()

    def call_event(self, event: Event, params: Tuple):

        try:

            if event == Event.MESSAGE_RECEIVED and self.message_received is not None:
                check_type("event", params, Tuple[str, str])
                self.message_received(params[0], params[1])

        except TypeError:
            _system.get_logger().debug(f"incorrect parameter provided for event {event.name}")

    def __enter__(self):
        self.looper_thread.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def send_message(name: str, message: str):
    _action_buffer.append(Action(ActionName.SEND_MESSAGE, (name, message)))


def quit_supbot():
    _system.quit()
