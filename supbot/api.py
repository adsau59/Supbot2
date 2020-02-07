
from typing import Callable


from supbot.model import Action, ActionName, Event
from supbot.system import System


class Supbot:
    def __init__(self, message_received: Callable[['Supbot', str, str], None] = None):
        self._system = System(self)

        self.message_received = message_received

    @property
    def events(self):
        return {
            Event.MESSAGE_RECEIVED: self.message_received
        }

    def __enter__(self):
        self._system.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._system.quit()
        self._system.wait_for_finish()

    def wait_for_finish(self):
        self._system.wait_for_finish()

    def quit(self):
        self._system.quit()

    def is_on(self):
        return self._system.is_on()

    def send_message(self, name: str, message: str):
        self._system.get_action_buffer().append(Action(ActionName.SEND_MESSAGE, (name, message)))
