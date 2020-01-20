from abc import ABC, abstractmethod
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
    def get_new_chat(self) -> model.Chat:
        pass
