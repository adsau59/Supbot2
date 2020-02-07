import typing
from enum import Enum
from typing import Tuple, Callable, List
from typing import NamedTuple

from supbot.app_driver import AppDriver

if typing.TYPE_CHECKING:
    from supbot.api import System


class State(Enum):
    MAIN = 0,
    CHAT = 1


class Event(Enum):
    MESSAGE_RECEIVED = 0


class ActionName(Enum):
    SEND_MESSAGE = 0


class Chat(NamedTuple):
    name: str


class GUIState(NamedTuple):
    state: State
    info: str = ""


class Action(NamedTuple):
    name: ActionName
    data: Tuple


class ActionMeta(NamedTuple):
    data_type: type
    run: Callable[[AppDriver, GUIState, 'System', Tuple], GUIState]  # (driver, state, data) -> state


ActionBuffer = List[Action]
