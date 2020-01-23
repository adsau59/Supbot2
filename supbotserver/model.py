from enum import Enum
from typing import Tuple, Dict, Callable
from typing import NamedTuple


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
    from supbotserver.shared_states.app_driver import IDriver
    run: Callable[[IDriver, GUIState, Tuple], GUIState]  # (driver, state, data) -> state
    data_type: type


States = Dict[str, GUIState]
