from random import shuffle

from poker_engine.card import Card
from poker_engine.constants import Suit, Value


class CardDeck:
    """
    class for deck
    """

    CARDS_AMOUNT = 52
    """amount of cards in deck"""

    def __init__(self):
        self.__cards = [
            Card(suit, value)
            for suit in Suit
            for value in Value
        ]
        shuffle(self.__cards)

    @property
    def cards(self) -> list:
        return self.__cards

    def shuffle(self) -> None:
        """
        Тосовка
        """
        shuffle(self.__cards)

    def draw_card(self) -> Card:
        """
        Берем верхнюю карту
        """
        if not self.__cards:
            raise IndexError('Deck empty')
        return self.__cards.pop()

    def reset(self) -> None:
        """
        Ресетим колоду и мешаем
        """
        self.__init__()

    def __len__(self) -> int:
        return len(self.__cards)

    def __repr__(self) -> str:
        return f"<CardDeck ({len(self)} карт)>"
