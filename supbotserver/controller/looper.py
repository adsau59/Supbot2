from supbotserver.controller import action_helper
from supbotserver import model
from supbotserver.model import State
from supbotserver.sharedstates.action_buffer import IActionBuffer
from supbotserver.sharedstates.app_driver import AppDriver
from supbotserver.sharedstates.event import IEventHandler
from supbotserver.sharedstates.system import ISystem


def start_looper(action_buffer: IActionBuffer, event: IEventHandler,
                 system: ISystem):
    action_helper.initialize()

    d = AppDriver()
    gui_state = model.GUIState(State.MAIN)

    system.get_logger().info("Started")

    while system.get_status():

        if action_buffer.size() == 0:
            gui_state = action_helper.check_for_new_chat(d, gui_state, event, system)
        else:
            gui_state = action_helper.execute_action(d, gui_state, action_buffer, system)
