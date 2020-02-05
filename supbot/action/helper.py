import typing

from typeguard import check_type

from supbot.action.functions import actions
from supbot.model import State, ActionBuffer, GUIState, Chat, Action, Event
from supbot.app_driver import IDriver
from supbot.system import ISystem

if typing.TYPE_CHECKING:
    from supbot.api import IEventHandler

# checker actions
def check_for_new_chat(system: ISystem, driver: IDriver,
                       event: 'IEventHandler', current: GUIState) -> GUIState:
    current = change_state(driver, current, GUIState(State.MAIN), system)
    chat = driver.get_new_chat()
    if chat is not None:
        current = check_for_new_messages(system, driver, event, chat, current)
    return current


def check_for_new_messages(system: ISystem, driver: IDriver,
                           event: 'IEventHandler', chat: Chat, current: GUIState) -> GUIState:
    current = change_state(driver, current, GUIState(State.CHAT, chat.name), system)
    messages = driver.get_new_messages()

    event.call_event(Event.MESSAGE_RECEIVED, (chat.name, list(messages)))

    return current


# action helper
def execute_action(driver: IDriver, buffer: ActionBuffer, current: GUIState,
                   system: ISystem) -> GUIState:
    try:
        action: Action = buffer.pop()
    except IndexError:
        return current

    meta = actions[action.name]

    try:
        check_type(action.name.name, action.data, meta.data_type)
    except TypeError:
        system.get_logger().warning(f"Action Data Typing incorrect for {action.name} "
                                    f": got {action.data} expected {meta.data_type}")

        return current

    current = meta.run(driver, current, system, action.data)
    return current


def change_state(driver: IDriver, _from: GUIState, _to: GUIState, system: ISystem) -> GUIState:
    if _to.state == State.MAIN:

        if _from.state == State.CHAT:
            driver.press_back()

    elif _to.state == State.CHAT:

        if _from.state == State.MAIN:

            if not driver.click_on_chat(_to.info):
                system.get_logger().warning(f"Couldn't switch to {_to.state.name}:{_to.info} "
                                            f"from {_from.state.name}:{_from.info}'")
                return _from

        elif _from.state == State.CHAT and _from.info != _to.info:
            driver.press_back()
            driver.click_on_chat(_to.info)

    return _to
