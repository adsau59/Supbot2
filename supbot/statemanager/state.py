from enum import Enum

from typing import Tuple, cast

from abc import ABC

from supbot import g
from supbot.results import GotoStateResult


class State(Enum):
    """
    Represents different states of the gui in whatsapp app
    """
    MAIN = 0,
    CHAT = 1,
    SEARCH = 2


class GUIState(ABC):
    def __init__(self, state: State):
        self.state = state

    def check(self) -> bool:
        """
        Checks if the gui on this state or not
        :return: False if state is not same as the gui
        """
        ...

    def _to_state(self, target: 'GUIState') -> Tuple[GotoStateResult, 'GUIState']:
        """
        takes in a state and takes ONLY ONE step towards the target state,
        if the step is taken, success is returned
        :param target:
        :return:
        """
        ...

    def to(self, target: 'GUIState') -> Tuple[GotoStateResult, 'GUIState']:
        result, current = self._to_state(target)

        if result == GotoStateResult.SUCCESS:
            if current.check():
                return result, current
            else:
                return GotoStateResult.CHECK_FAILED, current

        return result, current


class MainState(GUIState):
    def __init__(self):
        super().__init__(State.MAIN)
        self.scrolling = False

    def scroll_to_top(self):
        while not g.driver.check_scroll_top():
            g.driver.scroll_chat(reverse=True)
        self.scrolling = False

    def scroll_down(self):
        self.scrolling = True
        g.driver.scroll_chat()

    def check(self):
        return g.driver.check_fab()

    def _to_state(self, target: 'GUIState') -> Tuple[GotoStateResult, 'GUIState']:

        if target.state == State.MAIN:
            if self.scrolling:
                self.scroll_to_top()

            return GotoStateResult.SUCCESS, target

        elif target.state == State.SEARCH:
            if g.driver.click_search():
                return GotoStateResult.SUCCESS, target

        elif target.state == State.CHAT:
            if g.driver.click_on_chat(cast(ChatState, target).contact):
                return GotoStateResult.SUCCESS, target
            else:
                return GotoStateResult.ELEMENT_NOT_FOUND, self


class SearchState(GUIState):
    def __init__(self):
        super().__init__(State.SEARCH)

    def check(self):
        return g.driver.check_search_input()

    def _to_state(self, target: 'GUIState') -> Tuple[GotoStateResult, 'GUIState']:

        if target.state == State.MAIN:
            g.driver.press_search_back()
            return GotoStateResult.SUCCESS, target

        elif target.state == State.SEARCH:
            return GotoStateResult.SUCCESS, target

        elif target.state == State.CHAT:
            chat_name = cast(ChatState, target).contact
            if g.driver.type_in_search(chat_name) and g.driver.click_on_chat(chat_name, True):
                return GotoStateResult.SUCCESS, target
            else:
                return GotoStateResult.ELEMENT_NOT_FOUND, self


class ChatState(GUIState):
    def __init__(self, contact):
        super().__init__(State.CHAT)
        self.contact = contact

    def check(self):
        return g.driver.check_chat(self.contact)

    def _to_state(self, target: 'GUIState') -> Tuple[GotoStateResult, 'GUIState']:
        if target.state == State.MAIN:
            g.driver.press_chat_back()
            return GotoStateResult.SUCCESS, target

        elif target.state == State.SEARCH:
            g.driver.press_search_back()
            return GotoStateResult.SUCCESS, main_state

        elif target.state == State.CHAT:
            if cast(ChatState, target).contact == self.contact:
                return GotoStateResult.SUCCESS, self
            else:
                g.driver.press_chat_back()
                return GotoStateResult.SUCCESS, main_state


main_state = MainState()
search_state = SearchState()
temp_group = ChatState("!temp")
