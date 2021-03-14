import re
from typing import Tuple, cast

from supbot import g
from supbot.results import GotoStateResult
from supbot.statemanager.state import GUIState, State, ChatState, search_state, temp_group, main_state


def goto_state(_current: GUIState, _to: GUIState) -> Tuple[GotoStateResult, GUIState]:
    """
    Public interface for transitioning from one phase to the next,
    calls `_step_to_state` which breaks down the target into small steps by calling itself recursively,

    for ex.
    if current = Main state & _to = chat which isn't in main screen,
    it will first call goto(main, search)
    then it will call goto(search, chat)

    :param _current: current state
    :param _to: target state
    :return: (result, current_state)
    """
    g.logger.debug(f"going from state {_current.state} to {_to.state}")
    result, new_current = _step_to_state(_current, _to)

    if result == GotoStateResult.CHECK_FAILED:
        g.logger.error("De-synced trying to go from {} to {}".format(_current.state, _to.state))

    return result, new_current


def _step_to_state(_current: GUIState, _to: GUIState) -> Tuple[GotoStateResult, GUIState]:
    """
    When called, this function will make sure that the gui reaches the target state;
    if it couldn't, it'll return the error code
    recursively calls itself until target state has been reached

    if it can't reach the state directly, it will step to state it can go to next to reach the target,
    it will do so until the target stat is reached

    successful step:    bot performed some action on the ui,
                        and it reached another state (not necessarily the target state) successfully
                        result code: SUCCESS

    unsuccessful step:  bot tried to perform some action on the ui,
                        but it wasn't able to for either of these two reasons (result code)

    ELEMENT_NOT_FOUND: UI was able to find the ui element to perform the action
                        solution: use fallbacks or return fail

    CHECK_FAILED     : bot performed the action on the UI but
                       the state reached wasn't able to verify
                       solution: return fail and reset UI to main
                                (as bot doesn't know how to get back from unknown states)

    :param _current: current state
    :param _to: target state
    :return: (result, current_state)
    """

    # initial check if the starting state is correct
    if not _current.check():
        g.logger.debug(f"{_current.state} state check failed")
        _check_failed()
        return GotoStateResult.CHECK_FAILED, main_state

    # try to go to the target state
    g.logger.debug(f"Trying to step towards next state")
    result, new_current = _current.to(_to)

    # The step was successful,
    if result == GotoStateResult.SUCCESS:
        g.logger.debug(f"step was successful")

        # if the target state has been reached, return the function
        if new_current.state == _to.state:
            g.logger.debug(f"reached target state")

            # if the target is not chat, target state as been reached
            if new_current.state != State.CHAT:
                return result.SUCCESS, _to

            # extra check for chat state (each chat state is unique, different state for each contact)
            if cast(ChatState, new_current).contact and cast(ChatState, _to).contact:
                return result.SUCCESS, _to

            # just to be safe, return out of if statement
            return _step_to_state(new_current, _to)

        else:
            # if the target state is not reached, (even though the step was successful)
            # that means a step towards the target was taken
            g.logger.debug(f"reached intermediary state")
            return _step_to_state(new_current, _to)

    # The step was unsuccessful
    elif result == GotoStateResult.ELEMENT_NOT_FOUND:
        g.logger.debug(f"step was unsuccessful with result {result}")

        # try to use fallbacks for chat state
        if _to.state == State.CHAT:
            g.logger.debug(f"trying fallbacks for chat target state")
            return _goto_chat_fallback(new_current, _to)

        # else just return fail
        return result, _current

    # if the check failed, reset the ui and give a warning
    if result == GotoStateResult.CHECK_FAILED:
        g.logger.debug(f"step was unsuccessful with result {result}")
        _check_failed()
        return result, main_state

    # just to be safe, return out of if statement
    return result, _current


def _goto_chat_fallback(_current: GUIState, _to: GUIState) -> Tuple[GotoStateResult, GUIState]:
    """
    this is used, when chat is not found on the main screen, when the message has to be sent,
    when that happens bot tries to search for the contact first,
    if its still not found in search, it then creates a wa.me link using !temp group if the contact is a phone number
    :param _current: current state of the gui
    :param _to: ChatState to reach
    :return: (result, current_state)
    """
    # here it is ok to assume that `_to` type is Chat
    chat: ChatState = cast(ChatState, _to)

    # goto search state (to search the chat)
    g.logger.debug("trying to search for chat")
    result, new_current = _step_to_state(_current, search_state)

    if result == GotoStateResult.SUCCESS:

        # type in the name and click on the chat
        result, new_current = new_current.to(chat)

        # if chat found then good enough
        if result == GotoStateResult.SUCCESS:
            g.logger.debug("chat found by search")
            return result, new_current

        # if not found, then use temp group search method if it is a phone number
        elif result == GotoStateResult.ELEMENT_NOT_FOUND:
            g.logger.debug("couldn't find chat by search, checking if its a phone number")
            contact = cast(ChatState, chat).contact
            if not re.search(r"\d{8,13}", contact):
                g.logger.debug("not a phone number, returning fail")
                return result, new_current

            g.logger.debug("going to temp group")
            result, new_current = _step_to_state(new_current, temp_group)

            if result == GotoStateResult.SUCCESS:
                g.logger.debug("writing wa.me link")
                if g.driver.type_and_send(f"wa.me/{contact}", False) and g.driver.click_on_last_chat_link():
                    if not g.driver.click_ok():
                        return GotoStateResult.SUCCESS, chat

    # if nothing works then just return the current state
    return result, new_current


def _check_failed():
    """
    Give error and reset the UI to Main state
    """
    g.logger.error("UI DESYNCED :( THIS SHOULD NOT HAPPEN, CONTACT THE DEV IF ITS REPRODUCIBLE")
    g.logger.info("restarting whatsapp")
    g.driver.goto_home()
