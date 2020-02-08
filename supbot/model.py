"""
model.py

Contains all the models used in different systems of supbot
"""

import typing
from enum import Enum
from typing import Tuple, Callable, List
from typing import NamedTuple
from supbot.app_driver import AppDriver

if typing.TYPE_CHECKING:
    from supbot.api import System


class State(Enum):
    """
    Represents different states of the gui in whatsapp app
    """
    MAIN = 0,
    CHAT = 1


class Event(Enum):
    """
    Names of all the event that supbot supports
    events are functions executed when something occurs in whatsapp
    """
    MESSAGE_RECEIVED = 0


class ActionName(Enum):
    """
    Names of all the actions that supbot supports
    actions are functions executed upon request from the developer
    """
    SEND_MESSAGE = 0


class Chat(NamedTuple):
    """
    Encapsulation for chat
    for now just accepts
    """
    name: str


class GUIState(NamedTuple):
    """
    Encapsulates the GUI State and data which represent the current state in which the GUI is
    """
    state: State
    info: str = ""


class Action(NamedTuple):
    """
    Encapsulates the action name, and the data required to perform it
    """
    name: ActionName
    data: Tuple


class ActionMeta(NamedTuple):
    """
    Encapsulates the meta data of action, which contains the method required to run the action and the type of the
    parameter it takes in
    """
    data_type: type
    run: Callable[[AppDriver, GUIState, 'System', Tuple], GUIState]  # (driver, state, data) -> state


"""
Assigning a name to list of actions for action buffer,
used to create action buffer in `System`
"""
ActionBuffer = List[Action]
