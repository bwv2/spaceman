import abc
from typing import Union


class Currency(metaclass=abc.ABCMeta):
    def __init__(self, symbol: str):
        self.symbol: str = symbol

    @abc.abstractmethod
    def is_valid_address(self, address: Union[str, bytes]) -> bool:
        raise NotImplementedError
