"""
action.py

Contains all the actions available
"""
from enum import Enum
from typing import Tuple, Dict, Callable

from supbot import g
from supbot.results import GotoStateResult
from supbot.statemanager.state import GUIState, ChatState, State
from supbot.statemanager.transition import goto_state


class ActionName(Enum):
    SEND_MESSAGE = 0


def send_message(current: GUIState, data: Tuple) -> Tuple[bool, GUIState]:
    """
    Sends message to the target contact

    :param current: Current GUI state
    :param data: Data required to execute the service
    :return: resultant gui state after executing the action
    """
    chat_name, message = data

    result, current = goto_state(current, ChatState(chat_name))

    if result == GotoStateResult.SUCCESS and current.state == State.CHAT:
        g.driver.type_and_send(message)
        return True, current
    else:
        g.logger.warning("Failed to send message to {}".format(message, chat_name))
        return False, current


"""
Mapping action name to the action method and also the type of the data it takes in
"""
actions: Dict[ActionName, Callable] = {
    ActionName.SEND_MESSAGE: send_message
}
