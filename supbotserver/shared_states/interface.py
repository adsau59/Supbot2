from abc import ABC, abstractmethod
from typing import Tuple, Optional

from supbotserver import model


class IDriver(ABC):

    @abstractmethod
    def destroy(self):
        pass

    @abstractmethod
    def click_on_chat(self, chat_name: str):
        pass

    @abstractmethod
    def type_and_send(self, message: str):
        pass

    @abstractmethod
    def press_back(self):
        pass

    @abstractmethod
    def get_new_chat(self) -> Optional[model.Chat]:
        pass

    @abstractmethod
    def get_new_messages(self) -> Optional[Tuple[str]]:
        pass


class IClient(ABC):

    @abstractmethod
    def send_new_message(self, chat: model.Chat, message: str):
        pass


class IEventHandler(ABC):

    @abstractmethod
    def new_messages(self, chat: model.Chat, messages: Tuple[str]):
        pass


class IActionBuffer(ABC):

    @abstractmethod
    def get_action(self) -> model.Action:
        pass

    @abstractmethod
    def add_action(self, action: model.Action):
        pass

    @abstractmethod
    def size(self):
        pass


class ISystem(ABC):

    @abstractmethod
    def get_status(self) -> bool:
        pass

    @abstractmethod
    def set_status(self, status:bool):
        pass

    @abstractmethod
    def wait(self):
        pass
