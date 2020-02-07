import typing

from supbot import model
from supbot.action import helper
from supbot.model import State
from supbot.app_driver import AppDriver

if typing.TYPE_CHECKING:
    from supbot.api import System


def start(system: 'System'):
    driver = AppDriver()
    gui_state = model.GUIState(State.MAIN)

    system.get_logger().info("Started")

    while system.is_on() and len(system.get_action_buffer()) > 0:

        if len(system.get_action_buffer()) == 0:
            gui_state = helper.check_for_new_chat(system, driver, gui_state)
        else:
            gui_state = helper.execute_action(system, driver, gui_state)
