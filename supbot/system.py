"""
system.py

provides services to different systems of supbot,
contains `System` class
"""

import logging
import threading
import typing
from typing import Tuple, Dict
from supbot import looper, g
from supbot.action import Action
from supbot.app_driver import AppDriver
from supbot.service_manager import Event

if typing.TYPE_CHECKING:
    from supbot.api import Supbot

ActionBuffer = Dict[str, Action]


# noinspection PyMethodMayBeStatic
class System:
    """
    maintains shared states, and makes different states work together,
    provides interface to `Supbot` to control internal systems of supbot
    """

    def __init__(self, supbot: 'Supbot'):
        """
        Initialize shared states: action buffer, logger, status, which is used for different systems to comunicate
        initializes looper thread
        :param supbot: reference for the `Supbot` object, used to retrieve events at runtime
        """

        class PrintStreamHandler(logging.StreamHandler):
            def __init__(self):
                logging.StreamHandler.__init__(self)

            def emit(self, record):
                msg = self.format(record)
                print(msg)

        self.verbose = "verbose" in g.kwargs and g.kwargs["verbose"] is not None

        logging.getLogger("selenium").setLevel(logging.ERROR)
        logging.getLogger("urllib3").setLevel(logging.ERROR)
        logging.getLogger("appium").setLevel(logging.DEBUG)

        logging.basicConfig(level=logging.DEBUG if self.verbose else logging.INFO)

        logging.getLogger().handlers = []

        g.logger = logging.getLogger("supbot")
        log_format = "%(name)s - %(levelname)s - %(message)s"
        handler = PrintStreamHandler()
        handler.setFormatter(logging.Formatter(fmt=log_format))
        g.logger.addHandler(handler)

        if self.verbose:
            appium_logs = logging.getLogger('appium')
            fh = logging.FileHandler('appium.log', encoding='utf-8')
            appium_logs.addHandler(fh)

        """
        1: not started
        2: looper started
        0: quit requested
        -1: looper finished
        -2: appium finished
        """
        self.status = 1

        self._action_buffer: ActionBuffer = {}
        self._looper_thread = threading.Thread(target=looper.start)
        self._supbot = supbot
        g.system = self
        g.driver = AppDriver.create()

    @property
    def action_buffer(self) -> ActionBuffer:
        """
        Provides action buffer,
        Used to add actions in the queue by `Supbot`,
        used to get actions to perform by `looper.py`
        :return: ActionBuffer object (list of actions)
        """
        return self._action_buffer

    def start(self):
        """
        Starts the looper thread,
        used by `Supbot` to start its services (to make them usable)
        """
        self._looper_thread.start()

    def wait_for_finish(self):
        """
        Waits for the looper thread to finish,
        looper thread finishes when,  `_status` flag is False and there are no actions left in `_action_buffer`
        """
        self._looper_thread.join()
        if g.driver.appium_thread is not None:
            g.driver.appium_thread.join()

    def quit(self):
        """
        Turns `_status` flag False
        used to tell other systems, that supbot has to be turned off
        """
        self.status = 0

    def call_event(self, event: Event, params: Tuple):
        """
        Used to internal part of supbot to call events
        :param event: model.Event enum value
        :param params: data send for the event
        """
        callback = self._supbot.events[event]
        if callback is not None:
            threading.Thread(target=callback, args=params).start()

    def is_on(self) -> bool:
        """
        Used to check `_status` flag
        :return: `_status` flag
        """
        return self.status > 0

    def has_started(self) -> bool:
        """
        Used to check `_status` flag
        :return: `_status` flag
        """
        return self.status > 1
