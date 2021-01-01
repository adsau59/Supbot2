"""
api.py

Helps creating interface layer for the library,
abstracts the developer using supbot library from the underlying systems
"""
import time
import uuid
from typing import Callable, Dict, Optional

from supbot import g
from supbot.action import ActionName, Action, ActionCallback
from supbot.results import ActionStatus
from supbot.service_manager import Event
from supbot.system import System


# noinspection PyMethodMayBeStatic
class Supbot:
    """
    Supbot

    Entry point for the library,
    `Supbot` does just 2 things:
    1) accepts event callbacks though the constructor, and
    2) provides methods to run actions,

    Uses `System` to start and stop the services to make it usable
    """
    def __init__(self, message_received: Callable[[str, str], None] = None,
                 group_message_received: Callable[[str, str, str], None] = None,
                 **kwargs):
        """
        Takes in event callbacks, initializes the `System` object

        :param device_name: name of the device you want to control, by default it fetches automatically
        :param message_received: normal text message event callback
        """
        g.kwargs = kwargs
        self.message_received = message_received
        self.group_message_received = group_message_received
        self._system = System(self)

    @property
    def events(self) -> Dict[Event, Callable]:
        """
        Maps events to methods for `System` to call appropriate method for event
        :return: dictionary
        """
        return {
            Event.MESSAGE_RECEIVED: self.message_received,
            Event.GROUP_MESSAGE_RECEIVED: self.group_message_received
        }

    def __enter__(self):
        """
        Starts the supbot services by calling `System.start`,
        you have to call this methods before using any of the action methods
        :return: `Supbot` object
        """
        self._system.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Safely exits `Supbot` by completing any of the pending actions in the buffer
        """
        self._system.quit()
        self._system.wait_for_finish()

    def wait_for_finish(self):
        """
        Waits for `System` services (looper thread) to finish,
        Can be used to wait for while `Supbot` services are running
        """
        self._system.wait_for_finish()

    def quit(self):
        """
        Flags to supbot to turn off
        """
        self._system.quit()

    def is_on(self) -> bool:
        """
        Returns the on flag
        :return: False if `quit` method is called before
        """
        return self._system.is_on()

    def has_started(self) -> bool:
        return self._system.has_started()

    def wait_for_action(self, action: Action) -> bool:
        # todo use coroutines instead of thread blocking
        while action.status == ActionStatus.WAITING:
            time.sleep(.1)
        return action.status == ActionStatus.SUCCESS

    def send_message(self, contact_name: str, message: str, mentions: bool = False,
                     action_complete_callback: Optional[ActionCallback] = None) -> Action:
        """
        Send Message action
        sends message to the contact

        :param mentions: use mentions (tagging) when @ is used in front of contact/number
        :param action_complete_callback:
        :param contact_name: name of the contact to send message
        :param message: message to send
        """
        # todo move this into system
        action_id = str(uuid.uuid4())
        action = Action(action_id, ActionName.SEND_MESSAGE, action_complete_callback, ActionStatus.WAITING,
                        (contact_name, message, mentions))
        self._system.action_buffer[action_id] = action
        return action
