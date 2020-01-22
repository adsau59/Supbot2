from supbotserver.controller import action, state
from supbotserver import model
from supbotserver.shared_states import app_driver, interface


def start_looper(action_buffer: interface.IActionBuffer, event: interface.IEventHandler,
                 system: interface.ISystem):
    d = app_driver.AppDriver()
    gui_state = model.GUIStateWithInfo(state.states["main"])
    while True:

        if action_buffer.size() == 0:
            gui_state = action.check_for_new_chat(d, gui_state, event)
        else:
            gui_state = action.execute_action(d, gui_state, action_buffer)

        if not system.get_status():
            return
