from typing import List, Dict
from typing import NamedTuple
    

class Chat(NamedTuple):
    name: str
    text_history: List[str]


class GUIState(NamedTuple):
    name: str


class GUIStateWithInfo(NamedTuple):
    state: GUIState
    info: str

States = Dict[str, GUIState]
