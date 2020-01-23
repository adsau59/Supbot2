from supbotserver import model
from supbotserver.model import Action
from abc import ABC, abstractmethod

from supbotserver.shared_states.action_buffer import IActionBuffer


class IClient(ABC):

    @abstractmethod
    def send_message(self, chat: str, message: str):
        pass


class Client(IClient):
    action_buffer: IActionBuffer

    def __init__(self, action_buffer):
        self.action_buffer = action_buffer

    def send_message(self, chat: str, message: str):
        self.action_buffer.add_action(Action("send_message", (chat, message)))
