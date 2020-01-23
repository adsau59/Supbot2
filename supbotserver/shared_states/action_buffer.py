from typing import List, Optional

from supbotserver import model
from abc import ABC, abstractmethod


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


class ActionBuffer(IActionBuffer):

    def __init__(self):
        self.buffer: List[model.Action] = []

    def get_action(self) -> Optional[model.Action]:
        if self.size() > 0:
            return self.buffer.pop()
        return None

    def add_action(self, action: model.Action):
        self.buffer.append(action)

    def size(self):
        return len(self.buffer)
