"""
action.py

Contains all the actions available
"""
from dataclasses import dataclass
from enum import Enum
from typing import Tuple, Dict, Callable

from supbot import g
from supbot.results import GotoStateResult, ActionStatus
from supbot.statemanager.state import GUIState, ChatState, State
from supbot.statemanager.transition import goto_state


class ActionName(Enum):
    SEND_MESSAGE = 0


@dataclass
class Action:
    action_id: str
    action_name: ActionName
    callback: 'ActionCallback'
    status: ActionStatus
    data: Tuple

    def __repr__(self):
        return f"{self.action_name}: {self.data}: {self.status}"

    @property
    def success(self):
        return self.status == ActionStatus.SUCCESS


ActionCallback = Callable[[Action], None]


def send_message(current: GUIState, data: Tuple) -> Tuple[bool, GUIState]:
    """
    Sends message to the target contact

    :param current: Current GUI state
    :param data: Data required to execute the service
    :return: resultant gui state after executing the action
    """
    chat_name, message, mentions = data

    result, current = goto_state(current, ChatState(chat_name))

    if result == GotoStateResult.SUCCESS and current.state == State.CHAT and g.driver.type_and_send(message, mentions):
        return True, current
    else:
        g.logger.warning("Failed to send message to {}".format(chat_name))
        return False, current


"""
Mapping action name to the action method and also the type of the data it takes in
"""
actions: Dict[ActionName, Callable] = {
    ActionName.SEND_MESSAGE: send_message
}
