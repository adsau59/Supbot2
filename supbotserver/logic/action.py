from supbotserver import model, state
from supbotserver.controller import idriver
from typing import Tuple


def send_message(driver: idriver.IDriver, current: model.GUIStateWithInfo, chat: model.Chat,
                 message: str) -> model.GUIStateWithInfo:
    s = goto_chat(driver, current, chat)
    driver.type_and_send(message)
    return s


def goto_chat(driver: idriver.IDriver, current: model.GUIStateWithInfo, chat: model.Chat) -> model.GUIStateWithInfo:
    return state.change_state(driver, current, model.GUIStateWithInfo(state.states["chat"], chat.name))


def check_for_new_chat(driver: idriver.IDriver,
                       current: model.GUIStateWithInfo) -> Tuple[model.Chat, model.GUIStateWithInfo]:
    new_state = state.change_state(driver, current, model.GUIStateWithInfo(state.states["main"], ""))
    chat = driver.get_new_chat()
    return chat, new_state

