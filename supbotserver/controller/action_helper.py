from typeguard import check_type
from supbotserver import model, server
from supbotserver.model import State, actions
from supbotserver.sharedstates.action_buffer import IActionBuffer
from supbotserver.sharedstates.app_driver import IDriver
from supbotserver.sharedstates.system import ISystem
from supbotserver.controller.actions import send_message


def initialize():
    send_message.add()


# checker actions
def check_for_new_chat(driver: IDriver, current: model.GUIState,
                       system: ISystem) -> model.GUIState:
    current = change_state(driver, current, model.GUIState(State.MAIN), system)
    chat = driver.get_new_chat()
    if chat is not None:
        current = check_for_new_messages(driver, current, chat, system)
    return current


def check_for_new_messages(driver: IDriver, current: model.GUIState, chat: model.Chat,
                           system: ISystem) -> model.GUIState:
    current = change_state(driver, current, model.GUIState(State.CHAT, chat.name), system)
    messages = driver.get_new_messages()

    server.send_event("new_message", {"chat_name": chat.name, "message": list(messages)})

    return current


# action helper
def execute_action(driver: IDriver, buffer: IActionBuffer, current: model.GUIState,
                   system: ISystem) -> model.GUIState:
    action: model.Action = buffer.get_action()

    if action is None:
        return current

    meta = actions[action.name]

    try:
        check_type(action.name, action.data, meta.data_type)
    except TypeError:
        system.get_logger().warning(f"Action Data Typing incorrect for {action.name} "
                                    f": got {action.data} expected {meta.data_type}")

        return current

    current = meta.run(driver, current, system, action.data)
    return current


def change_state(driver: IDriver, _from: model.GUIState, _to: model.GUIState, system: ISystem) -> model.GUIState:
    if _to.state == State.MAIN:

        if _from.state == State.CHAT:
            driver.press_back()

    elif _to.state == State.CHAT:

        if _from.state == State.MAIN:

            if not driver.click_on_chat(_to.info):
                system.get_logger().warning(f"Couldn't switch to {_to.state.name}:{_to.info} "
                                            f"from {_from.state.name}:{_from.info}'")
                return _from

        elif _from.state == State.CHAT and _from.info != _to.info:
            driver.press_back()
            driver.click_on_chat(_to.info)

    return _to
