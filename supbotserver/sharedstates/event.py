from abc import ABC, abstractmethod
from typing import Tuple

from supbotserver import model


class IEventHandler(ABC):

    @abstractmethod
    def new_messages(self, chat: model.Chat, messages: Tuple[str]):
        pass


class EventHandler(IEventHandler):
    def new_messages(self, chat: model.Chat, messages: Tuple[str]):
        print(messages)
