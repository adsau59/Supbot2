"""
action.py

Contains all the actions available
"""

import typing
from typing import Tuple, Dict
from supbot import service_manager
from supbot.model import State, ActionMeta, GUIState, ActionName
from supbot.app_driver import AppDriver

if typing.TYPE_CHECKING:
    from supbot.api import System


def send_message(driver: AppDriver, current: GUIState, system: 'System', data: Tuple) -> GUIState:
    """
    Sends message to the target contact

    :param driver: AppDriver service
    :param current: Current GUI state
    :param system: System services
    :param data: Data required to execute the service
    :return: resultant gui state after executing the action
    """
    chat_name, message = data

    error, current = service_manager.change_state(system, driver, current, GUIState(State.CHAT, chat_name))

    if not error and current.state == State.CHAT:
        driver.type_and_send(message)
        system.logger.debug("sent message {} to {} successfully".format(message, chat_name))
    else:
        system.logger.debug("Message failed")

    return current


"""
Mapping action name to the action method and also the type of the data it takes in
"""
actions: Dict[ActionName, ActionMeta] = {
    ActionName.SEND_MESSAGE: ActionMeta(Tuple[str, str], send_message)
}
