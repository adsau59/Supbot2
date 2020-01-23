from __future__ import annotations

from abc import ABC, abstractmethod
import loguru


class ISystem(ABC):

    @abstractmethod
    def get_status(self) -> bool:
        pass

    @abstractmethod
    def set_status(self, status: bool):
        pass

    @abstractmethod
    def wait(self):
        pass

    @abstractmethod
    def get_logger(self) -> loguru.Logger:
        pass


class System(ISystem):

    def __init__(self):
        self.status = True
        self.logger = loguru.logger

    def get_status(self) -> bool:
        return self.status

    def set_status(self, status: bool):
        self.status = status

    def wait(self):
        input("enter to quit")

    def get_logger(self) -> loguru.Logger:
        return self.logger
