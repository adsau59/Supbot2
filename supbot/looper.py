import typing

from supbot import model
from supbot.action import helper
from supbot.model import State, ActionBuffer
from supbot.app_driver import AppDriver
from supbot.system import ISystem

if typing.TYPE_CHECKING:
    from supbot.api import IEventHandler


def start(buffer: ActionBuffer, event: 'IEventHandler', system: ISystem):
    driver = AppDriver()
    gui_state = model.GUIState(State.MAIN)

    system.get_logger().info("Started")

    while system.is_on():

        if len(buffer) == 0:
            gui_state = helper.check_for_new_chat(system, driver, event, gui_state)
        else:
            gui_state = helper.execute_action(driver, buffer, gui_state, system)
