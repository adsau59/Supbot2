"""
looper.py

provides a function which is initializes and maintains state of supbot
"""

from typing import Callable, List
import typing
from supbot import model, service_manager
from supbot.model import State
from supbot.app_driver import AppDriver

if typing.TYPE_CHECKING:
    from supbot.api import System

_test_function: List[Callable[[AppDriver, model.GUIState], None]] = []


def start(system: 'System', device_name: str):
    """
    initializes services which is used internally in supbot

    provides an update design which,
    1) executes action added in action buffer in each update
    2) if there are no actions, then run checkers
    (for now its just `manager.check_for_new_chat` but it'll be reworked to support multiple checkers)

    maintains `gui_state` which represents the state in which the app currently is in

    :param device_name: name of the device to be used
    :param system: provides services and shared states which is used internally
    """
    driver = AppDriver.create(device_name)

    if driver is None:
        system.logger.error("Driver couldn't be created successfully, maybe Appium is not running or your android "
                            "device couldn't be found")
        return

    gui_state = model.GUIState(State.MAIN)

    system.logger.info("Started")
    system.started()

    while system.is_on() or len(system.action_buffer) > 0:

        if len(system.action_buffer) == 0:
            gui_state = service_manager.check_for_new_chat(system, driver, gui_state)
        else:
            gui_state = service_manager.execute_action(system, driver, gui_state)

        if _test_function:
            _test_function.pop(0)(driver, gui_state)

    driver.destroy()
