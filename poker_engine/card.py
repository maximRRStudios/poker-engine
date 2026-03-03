"""
Модуль карты
"""
from .constants import Suit, Value

class Card:
    """
    class for card
    """

    def __init__(self, suit: Suit, value: Value):
        self.__suit = suit
        self.__value = value

    @property
    def suit(self) -> Suit:
        """
        getter for suit
        """
        return self.__suit

    @property
    def value(self) -> Value:
        """
        getter for value
        """
        return self.__value

    def __repr__(self):
        return f"{self.__value.name} of {self.__suit.name}"

    def __eq__(self, other: Card):
        if isinstance(other, Card):
            return self.__value == other.value
        return NotImplemented

    def __lt__(self, other: Card):
        if isinstance(other, Card):
            return self.__value.value < other.value.value
        return NotImplemented

    def __hash__(self):
        return hash((self.__suit, self.__value))
