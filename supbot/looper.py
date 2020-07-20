"""
looper.py

provides a function which is initializes and maintains state of supbot
"""

from supbot import service_manager, g
from supbot.statemanager.state import main_state

# _test_function: List[Callable[[AppDriver, model.GUIState], None]] = []


def start():
    """
    initializes services which is used internally in supbot

    provides an update design which,
    1) executes action added in action buffer in each update
    2) if there are no actions, then run checkers
    (for now its just `manager.check_for_new_chat` but it'll be reworked to support multiple checkers)

    maintains `gui_state` which represents the state in which the app currently is in
    """
    if g.driver is None:
        g.system.logger.error("Driver couldn't be created successfully, maybe Appium is not running or your android "
                            "device couldn't be found")
        return

    gui_state = main_state

    g.system.logger.info("Started")
    g.system.status = 2

    while g.system.is_on() or len(g.system.action_buffer) > 0:

        if len(g.system.action_buffer) == 0:
            gui_state = service_manager.check_for_new_chat(gui_state)
        else:
            gui_state = service_manager.execute_action(gui_state)

        # if _test_function:
        #     _test_function.pop(0)(driver, gui_state)

    g.driver.destroy()
    g.system.status = -1
