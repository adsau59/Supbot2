"""
manager.py

contains functions which performs operations (actions/checkers) on whatsapp app
they use `AppDriver` to perform it.

Checkers will get a rework to support other than `check_new_chat` eventually
"""

import typing
from typeguard import check_type
from supbot.action.functions import actions
from supbot.model import State, GUIState, Action, Event
from supbot.app_driver import AppDriver
if typing.TYPE_CHECKING:
    from supbot.api import System


# checker actions
def check_for_new_chat(system: 'System', driver: AppDriver,
                       current: GUIState) -> GUIState:
    """
    Checks for new chat on the main screen, first changes screen to main then uses driver to check it,
    if new chat is found, go into that chat and get the messages and call event for it

    :param system: `System` object
    :param driver: `AppDriver` object, used to perform operations on whatsapp gui
    :param current: data of current state of the app
    :return: resultant state of gui after operation
    """
    current = change_state(system, driver, current, GUIState(State.MAIN))
    chat = driver.get_new_chat()
    if chat is not None:
        current = change_state(system, driver, current, GUIState(State.CHAT, chat.name))
        messages = driver.get_new_messages()

        for m in messages:
            system.call_event(Event.MESSAGE_RECEIVED, (chat.name, m))
    return current


# action helper
def execute_action(system: 'System', driver: AppDriver, current: GUIState) -> GUIState:
    """
    Pop action from the buffer, and execute it, update the gui state
    :param system: `System` object
    :param driver: `AppDriver` object, used to perform operations on whatsapp gui
    :param current: current gui state
    :return: resultant state of gui after action is executed
    """
    try:
        action: Action = system.action_buffer.pop()
    except IndexError:
        return current

    meta = actions[action.name]

    try:
        check_type(action.name.name, action.data, meta.data_type)
    except TypeError:
        system.logger.warning(f"Action Data Typing incorrect for {action.name} : got {action.data} expected "
                              f"{meta.data_type}")

        return current

    current = meta.run(driver, current, system, action.data)
    return current


def change_state(system: 'System', driver: AppDriver, _from: GUIState, _to: GUIState) -> GUIState:
    """
    performs appropriate actions on the gui to reach the target gui state
    Changes gui state and returns the updated state object depending on success or failure
    :param system: `System` object
    :param driver: AppDriver` object, used to perform operations on whatsapp gui
    :param _from: current gui state
    :param _to: target gui state
    :return: resultant state of gui after
    """
    if _to.state == State.MAIN:

        if _from.state == State.CHAT:
            driver.press_back()

    elif _to.state == State.CHAT:

        if _from.state == State.MAIN:

            if not driver.click_on_chat(_to.info):
                system.logger.warning(f"Couldn't switch to {_to.state.name}:{_to.info} from {_from.state.name} : "
                                      f"{_from.info}'")
                return _from

        elif _from.state == State.CHAT and _from.info != _to.info:
            driver.press_back()
            driver.click_on_chat(_to.info)

    return _to
