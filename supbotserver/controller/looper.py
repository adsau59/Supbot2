from supbotserver.controller import action_helper
from supbotserver import model
from supbotserver.model import State
from supbotserver.sharedstates.action_buffer import IActionBuffer
from supbotserver.sharedstates.app_driver import AppDriver
from supbotserver.sharedstates.system import ISystem


def start(buffer: IActionBuffer, system: ISystem):
    action_helper.initialize()

    d = AppDriver()
    gui_state = model.GUIState(State.MAIN)

    system.get_logger().info("Started")

    while system.is_on():

        if buffer.size() == 0:
            gui_state = action_helper.check_for_new_chat(d, gui_state, system)
        else:
            gui_state = action_helper.execute_action(d, buffer, gui_state, system)
