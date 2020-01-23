from typing import Tuple, Any

from supbotserver.controller import action_helper
from supbotserver.model import State, Action, ActionMeta, actions, GUIState
from supbotserver.sharedstates.app_driver import IDriver
from supbotserver.sharedstates.system import ISystem


def run(driver: IDriver, current: GUIState, system: ISystem, data: Tuple) -> GUIState:
    chat_name, message = data

    current = action_helper.change_state(driver, current, GUIState(State.CHAT, chat_name), system)

    if current.state == State.CHAT:
        driver.type_and_send(message)

    return current


def json_to_action(json: Any) -> Action:
    return Action("send_message", (json["chat"], json["message"]))


def add():
    # data: (chat_name, message)
    actions["send_message"] = ActionMeta("send_message", Tuple[str, str], run, json_to_action)
