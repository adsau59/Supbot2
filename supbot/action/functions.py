from typing import Tuple, Dict

from supbot.action import helper
from supbot.model import State, ActionMeta, GUIState, ActionName
from supbot.app_driver import IDriver
from supbot.system import ISystem


def send_message(driver: IDriver, current: GUIState, system: ISystem, data: Tuple) -> GUIState:
    chat_name, message = data

    current = helper.change_state(driver, current, GUIState(State.CHAT, chat_name), system)

    if current.state == State.CHAT:
        driver.type_and_send(message)

    return current


actions: Dict[ActionName, ActionMeta] = {
    ActionName.SEND_MESSAGE: ActionMeta(Tuple[str, str], send_message)
}
