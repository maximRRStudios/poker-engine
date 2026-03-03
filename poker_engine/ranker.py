from abc import ABC, abstractmethod
from typing import Dict, List, Tuple, Union

from poker_engine.card import Card
from poker_engine.constants import Combination, Value


class HandValidator(ABC):
    @abstractmethod
    def validate(self, cards: List[Card]) -> Union[None, Combination]:
        pass


class RoyalFlushValidator(HandValidator):
    def validate(self, cards: List[Card]):
        pass


class StraightFlushValidator(HandValidator):
    def validate(self, cards: List[Card]):
        pass


class FourOfAKindValidator(HandValidator):
    def validate(self, cards: List[Card]):
        pass


class FullHouseValidator(HandValidator):
    def validate(self, cards: List[Card]):
        pass


class FlushValidator(HandValidator):
    def validate(self, cards: List[Card]):
        pass


class StraightValidator(HandValidator):
    def validate(self, cards: List[Card]):
        pass


class ThreeOfAKindValidator(HandValidator):
    def validate(self, cards: List[Card]):
        pass


class TwoPairsValidator(HandValidator):
    def validate(self, cards: List[Card]):
        pass


class OnePairValidator(HandValidator):
    def validate(self, cards: List[Card]):
        pass


class Ranker:

    def __init__(self) -> None:
        self.__validators = [
            RoyalFlushValidator(),
            StraightFlushValidator(),
            FourOfAKindValidator(),
            FullHouseValidator(),
            FlushValidator(),
            StraightValidator(),
            ThreeOfAKindValidator(),
            TwoPairsValidator(),
            OnePairValidator()
        ]

    def evaluate_hand(self, cards: List[Card]) -> Tuple[int, List[Card]]:
        """
        Оценивает силу руки и возвращает лучший набор карт и ранг комбинации.
        """
        hand = self.__sort_by_strength(cards)
        for validator in self.__validators:
            result = validator.validate(hand)
            if result:
                return result
        return (Combination.HIGH_CARD, hand[:5])

    def get_combination_name(self, rank: int) -> str:
        """Возвращает название комбинации по её рангу."""
        pass

    @staticmethod
    def is_straight(cards: List[Card]) -> bool:
        """Проверяет, образуют ли карты стрит."""

        pass

    @staticmethod
    def is_flush(cards: List[Card]) -> bool:
        """Проверяет, образуют ли карты флеш."""
        if len(cards) < 5:
            return False
        cd_dict = {}
        for card in cards:
            cd_dict[card.suit] = cd_dict.get(card.suit, 0) + 1
        return max(cd_dict.values()) >= 5 

    @staticmethod
    def find_pairs(cards: List[Card]) -> Dict[Value, int]:
        """Находит пары, триплеты и каре в списке карт."""
        cd_dict = {}
        for card in cards:
            cd_dict[card.value] = cd_dict.get(card.value, 0) + 1
        return {key: val for key, val in cd_dict.items() if val > 1}

    @staticmethod
    def __sort_by_strength(cards: List[Card]) -> List[Card]:
        """Сортирует карты по убыванию силы."""
        return sorted(cards, reverse=True)
