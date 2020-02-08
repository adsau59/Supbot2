"""
looper.py

provides a function which is initializes and maintains state of supbot
"""

import typing
from supbot import model
from supbot.action import manager
from supbot.model import State
from supbot.app_driver import AppDriver
if typing.TYPE_CHECKING:
    from supbot.api import System


def start(system: 'System'):
    """
    initializes services which is used internally in supbot

    provides an update design which,
    1) executes action added in action buffer in each update
    2) if there are no actions, then run checkers
    (for now its just `manager.check_for_new_chat` but it'll be reworked to support multiple checkers)

    maintains `gui_state` which represents the state in which the app currently is in

    :param system: provides services and shared states which is used internally
    """
    driver = AppDriver()
    gui_state = model.GUIState(State.MAIN)

    system.logger.info("Started")

    while system.is_on() and len(system.action_buffer) > 0:

        if len(system.action_buffer) == 0:
            gui_state = manager.check_for_new_chat(system, driver, gui_state)
        else:
            gui_state = manager.execute_action(system, driver, gui_state)

    driver.destroy()
