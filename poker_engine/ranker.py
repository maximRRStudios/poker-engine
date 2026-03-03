from typing import Dict, List, Tuple

from poker_engine.card import Card
from poker_engine.constants import Value


class Ranker:
    def evaluate_hand(self, cards: List[Card]) -> Tuple[int, List[Card]]:
        """Оценивает силу руки и возвращает лучший набор карт и ранг комбинации."""
        pass

    def compare_hands(self, hands: List[Tuple[int, List[Card]]]) -> List[int]:
        """Сравнивает несколько рук и возвращает индексы выигравших игроков."""
        pass

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
    def sort_by_strength(cards: List[Card]) -> List[Card]:
        """Сортирует карты по убыванию силы."""
        return sorted(cards, reverse=True)
