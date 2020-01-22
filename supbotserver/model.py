from typing import Tuple, Dict, Callable
from typing import NamedTuple


class Chat(NamedTuple):
    name: str


class GUIState(NamedTuple):
    name: str


class GUIStateWithInfo(NamedTuple):
    state: GUIState
    info: str = ""


class Action(NamedTuple):
    name: str
    data: Tuple


class ActionMeta(NamedTuple):
    from supbotserver.shared_states import interface
    run: Callable[[interface.IDriver, GUIStateWithInfo, Tuple], GUIStateWithInfo]
    data_type: type


States = Dict[str, GUIState]
