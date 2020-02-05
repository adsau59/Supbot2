from enum import Enum
from typing import Tuple, Callable, List
from typing import NamedTuple

from supbot.system import ISystem
from supbot.app_driver import IDriver


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
    run: Callable[[IDriver, GUIState, ISystem, Tuple], GUIState]  # (driver, state, data) -> state


ActionBuffer = List[Action]
