from __future__ import annotations

import threading
import typing
from typing import Tuple

import loguru

from supbot import looper
from supbot.model import ActionBuffer, Event

if typing.TYPE_CHECKING:
    from supbot.api import Supbot


class System:
    def __init__(self, supbot: 'Supbot'):
        self._action_buffer: ActionBuffer = []
        self._logger = loguru.logger
        self._status = True
        self._looper_thread = threading.Thread(target=looper.start, args=(self,))
        self._supbot = supbot

    def get_logger(self) -> loguru.Logger:
        return self._logger

    def get_action_buffer(self) -> ActionBuffer:
        return self._action_buffer

    def start(self):
        self._looper_thread.start()

    def wait_for_finish(self):
        self._looper_thread.join()

    def quit(self):
        self._status = False

    def call_event(self, event: Event, params: Tuple):
        callback = self._supbot.events[event]
        if callback is not None:
            callback(self, *params)

    def is_on(self) -> bool:
        return self._status
