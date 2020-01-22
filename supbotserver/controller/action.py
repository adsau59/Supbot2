from typing import Tuple, Dict
from typeguard import check_type
from supbotserver.controller import state
from supbotserver import model
from supbotserver.shared_states import interface


def execute_action(driver: interface.IDriver, current: model.GUIStateWithInfo,
                   action_buffer: interface.IActionBuffer) -> model.GUIStateWithInfo:
    action: model.Action = action_buffer.get_action()

    if action is None:
        return current

    meta = actions[action.name]

    try:
        check_type(action.name, action.data, meta.data_type)
    except TypeError:
        return current

    current = meta.run(driver, current, action)
    return current


# actions

def send_message(driver: interface.IDriver, current: model.GUIStateWithInfo, data: Tuple) -> model.GUIStateWithInfo:
    current = state.change_state(driver, current, model.GUIStateWithInfo(state.states["chat"], data[0]))
    driver.type_and_send(data[1])
    return current


actions: Dict[str, model.ActionMeta] = {
    "send_message": model.ActionMeta(send_message, Tuple[str, str]),
}


# checker actions

def check_for_new_chat(driver: interface.IDriver, current: model.GUIStateWithInfo,
                       event: interface.IEventHandler) -> model.GUIStateWithInfo:
    current = state.change_state(driver, current, model.GUIStateWithInfo(state.states["main"], ""))
    chat = driver.get_new_chat()
    if chat is not None:
        current = check_for_new_messages(driver, current, chat, event)
    return current


def check_for_new_messages(driver: interface.IDriver, current: model.GUIStateWithInfo, chat: model.Chat,
                           event: interface.IEventHandler) -> model.GUIStateWithInfo:
    current = state.change_state(driver, current, model.GUIStateWithInfo(state.states["chat"], chat.name))
    messages = driver.get_new_messages()

    event.new_messages(chat, messages)

    return current
