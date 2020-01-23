from supbotserver.controller import action
from supbotserver import model
from supbotserver.model import State
from supbotserver.shared_states.action_buffer import IActionBuffer
from supbotserver.shared_states.app_driver import AppDriver
from supbotserver.shared_states.event import IEventHandler
from supbotserver.shared_states.system import ISystem


def start_looper(action_buffer: IActionBuffer, event: IEventHandler,
                 system: ISystem):
    d = AppDriver()
    gui_state = model.GUIState(State.MAIN)

    while system.get_status():

        if action_buffer.size() == 0:
            gui_state = action.check_for_new_chat(d, gui_state, event)
        else:
            gui_state = action.execute_action(d, gui_state, action_buffer, system)
