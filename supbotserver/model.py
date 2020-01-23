from enum import Enum
from typing import Tuple, Callable, Any, Dict
from typing import NamedTuple

from supbotserver.sharedstates.system import ISystem


class State(Enum):
    MAIN = 0,
    CHAT = 1


class Chat(NamedTuple):
    name: str


class GUIState(NamedTuple):
    state: State
    info: str = ""


class Action(NamedTuple):
    name: str
    data: Tuple


class ActionMeta(NamedTuple):
    from supbotserver.sharedstates.app_driver import IDriver
    name: str
    data_type: type
    run: Callable[[IDriver, GUIState, ISystem, Tuple], GUIState]  # (driver, state, data) -> state
    json_to_action: Callable[[Any], Action]


# globals

actions: Dict[str, ActionMeta] = {}
