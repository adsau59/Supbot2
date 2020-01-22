from typing import Tuple

from supbotserver import model
from supbotserver.shared_states import interface


class EventHandler(interface.IEventHandler):
    def new_messages(self, chat: model.Chat, messages: Tuple[str]):
        print(messages)
