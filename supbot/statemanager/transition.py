import re
from typing import Tuple, cast

from supbot import g
from supbot.results import GotoStateResult
from supbot.statemanager.state import GUIState, State, ChatState, search_state, temp_group


def goto_chat_fallback(_current: GUIState, _to: GUIState) -> Tuple[GotoStateResult, GUIState]:
    """
    here it is ok to assume that `_to` type is Chat
    :param _current:
    :param _to:
    :return:
    """
    # todo improve readability
    
    result, new_current = goto_state(_current, search_state)

    if result == GotoStateResult.SUCCESS:
        result, new_current = new_current.to(_to)

        if result == GotoStateResult.SUCCESS:
            return result, new_current
        elif result == GotoStateResult.ELEMENT_NOT_FOUND:

            result, new_current = goto_state(new_current, temp_group)

            if result == GotoStateResult.SUCCESS:
                contact = cast(ChatState, _to).contact
                if re.search("\d{11,13}", contact):
                    if g.driver.type_and_send(f"wa.me/{contact}") and g.driver.click_on_last_chat_link():
                        if not g.driver.click_ok():
                            return GotoStateResult.SUCCESS, _to

    return result, new_current


def goto_state(_current: GUIState, _to: GUIState) -> Tuple[GotoStateResult, GUIState]:
    """
    When called, this function will make sure that the gui reaches the target state;
    if it could, it'll return the error code
    :param _current:
    :param _to:
    :return:
    """
    if _current == _to:
        return GotoStateResult.SUCCESS, _to

    result, new_current = _current.to(_to)

    if result == GotoStateResult.SUCCESS:
        """
        The step was successful,
        either return success, or take the next step
        """
        # todo improve readability
        if new_current.state == _to.state:
            if new_current.state != State.CHAT:
                return result.SUCCESS, _to

            if cast(ChatState, new_current).contact and cast(ChatState, _to).contact:
                return result.SUCCESS, _to

            return goto_state(new_current, _to)

        else:
            return goto_state(_current, _to)
    elif result == GotoStateResult.ELEMENT_NOT_FOUND:
        """
        The step was unsuccessful,
        either return unsuccessful, or use fallbacks
        """
        if _to.state == State.CHAT:
            return goto_chat_fallback(new_current, _to)
        else:
            return GotoStateResult.ELEMENT_NOT_FOUND, _current

    if result == GotoStateResult.CHECK_FAILED:
        g.logger.error("UI desynced run the script again...")

    return result, _current
