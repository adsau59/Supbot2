from enum import Enum


class GotoStateResult(Enum):
    """
    When goto state successfully does its operation,
    even if it doesnt reach the `to` state (as it might just take one step sometimes`
    """
    SUCCESS = 0,

    """
    When element is not found
    """
    ELEMENT_NOT_FOUND = 1,

    """
    When check fails
    """
    CHECK_FAILED = 2
