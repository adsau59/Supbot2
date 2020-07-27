"""
service_manager.py

contains functions which performs operations (actions/checkers) on whatsapp app
they use `AppDriver` to perform it.

Checkers will get a rework to support other than `check_new_chat` eventually
"""
from enum import Enum

from supbot import g
from supbot.action import actions
from supbot.results import ActionStatus
from supbot.statemanager.state import main_state, GUIState, ChatState
from supbot.statemanager.transition import goto_state


class Event(Enum):
    MESSAGE_RECEIVED = 0


# checker
def check_for_new_chat(current: GUIState) -> GUIState:
    """
    Checks for new chat on the main screen, first changes screen to main then uses driver to check it,
    if new chat is found, go into that chat and get the messages and call event for it

    :param current: data of current state of the app
    :return: resultant state of gui after operation
    """
    _, current = goto_state(current, main_state)
    chat = g.driver.get_new_chat()
    if chat is not None:
        _, current = goto_state(current, ChatState(chat))
        messages = g.driver.get_new_messages()

        for m in messages:
            g.system.call_event(Event.MESSAGE_RECEIVED, (chat, m))
    return current


# action helper
def execute_action(current: GUIState) -> GUIState:
    """
    Pop action from the buffer, and execute it, update the gui state
    :param current: current gui state
    :return: resultant state of gui after action is executed
    """
    try:
        action_id, action = g.system.action_buffer.popitem()
    except IndexError:
        return current

    print("running action")

    success, current = actions[action.action_name](current, action.data)

    action.status = ActionStatus.SUCCESS if success else ActionStatus.UNSUCCESS

    if action.callback:
        action.callback(action_id)

    return current

