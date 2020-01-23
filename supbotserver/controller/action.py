from typing import Tuple, Dict
from typeguard import check_type
from supbotserver import model
from supbotserver.model import State
from supbotserver.shared_states.action_buffer import IActionBuffer
from supbotserver.shared_states.app_driver import IDriver
from supbotserver.shared_states.event import IEventHandler
from supbotserver.shared_states.system import ISystem


# actions
def send_message(driver: IDriver, current: model.GUIState, data: Tuple) -> model.GUIState:
    chat_name, message = data

    current = change_state(driver, current, model.GUIState(State.CHAT, chat_name))
    driver.type_and_send(message)
    return current


actions: Dict[str, model.ActionMeta] = {
    "send_message": model.ActionMeta(send_message, Tuple[str, str]),  # data: name, message
}


# checker actions
def check_for_new_chat(driver: IDriver, current: model.GUIState,
                       event: IEventHandler) -> model.GUIState:
    current = change_state(driver, current, model.GUIState(State.MAIN))
    chat = driver.get_new_chat()
    if chat is not None:
        current = check_for_new_messages(driver, current, chat, event)
    return current


def check_for_new_messages(driver: IDriver, current: model.GUIState, chat: model.Chat,
                           event: IEventHandler) -> model.GUIState:
    current = change_state(driver, current, model.GUIState(State.CHAT, chat.name))
    messages = driver.get_new_messages()

    event.new_messages(chat, messages)

    return current


# action helper
def execute_action(driver: IDriver, current: model.GUIState,
                   action_buffer: IActionBuffer, system:ISystem) -> model.GUIState:
    action: model.Action = action_buffer.get_action()

    if action is None:
        return current

    meta = actions[action.name]

    try:
        check_type(action.name, action.data, meta.data_type)
    except TypeError:
        system.get_logger().warning(f"Action Data Typing incorrect for {action.name} "
                                    f": got {action.data} expected {meta.data_type}")

        return current

    current = meta.run(driver, current, action)
    return current


def change_state(driver: IDriver, _from: model.GUIState, _to: model.GUIState) -> model.GUIState:
    if _to.state == State.MAIN:

        if _from.state == State.CHAT:
            driver.press_back()

    elif _to.state == State.CHAT:

        if _from.state == State.MAIN:
            driver.click_on_chat(_to.info)
        elif _from.state == State.CHAT and _from.info != _to.info:
            driver.press_back()
            driver.click_on_chat(_to.info)

    return _to
