import typing
from typing import Tuple, Dict

from supbot.action import helper
from supbot.model import State, ActionMeta, GUIState, ActionName
from supbot.app_driver import AppDriver

if typing.TYPE_CHECKING:
    from supbot.api import System


def send_message(driver: AppDriver, current: GUIState, system: 'System', data: Tuple) -> GUIState:
    chat_name, message = data

    current = helper.change_state(system, driver, current, GUIState(State.CHAT, chat_name))

    if current.state == State.CHAT:
        driver.type_and_send(message)

    return current


actions: Dict[ActionName, ActionMeta] = {
    ActionName.SEND_MESSAGE: ActionMeta(Tuple[str, str], send_message)
}
