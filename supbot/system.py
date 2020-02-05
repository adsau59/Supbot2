from __future__ import annotations

from abc import ABC, abstractmethod
import loguru


class ISystem(ABC):
    """
    System should only contain third party libraries
    which is going to used by every systems
    """

    @abstractmethod
    def is_on(self) -> bool:
        pass

    @abstractmethod
    def quit(self):
        pass

    @abstractmethod
    def wait(self):
        pass

    @abstractmethod
    def get_logger(self) -> loguru.Logger:
        pass


class System(ISystem):

    def __init__(self, logger: loguru.Logger):
        self.status = True
        self.logger = logger

    def is_on(self) -> bool:
        return self.status

    def wait(self):
        input("enter to quit")

    def get_logger(self) -> loguru.Logger:
        return self.logger

    def quit(self):
        self.status = False
