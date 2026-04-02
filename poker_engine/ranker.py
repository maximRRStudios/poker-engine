from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List, Tuple, Union, NamedTuple

from poker_engine.card import Card
from poker_engine.constants import Combination, Value


class HandEvaluationResult(NamedTuple):
    """
    Результат оценки покерной руки.
    
    Атрибуты:
        combination (Combination): Тип комбинации (например, Флеш, Сет и т.д.)
        cards (List[Card]): Лучшие 5 карт, составляющие комбинацию.
                           Отсортированы по значимости (от старшей к младшей).
    """
    combination: Combination
    cards: List[Card]


class HandValidator(ABC):
    """
    Абстрактный базовый класс для валидаторов покерных комбинаций.

    Каждый конкретный валидатор проверяет наличие определённой комбинации
    (например, флеш, стрит, каре и т.д.) в переданном наборе карт.
    """
    @abstractmethod
    def validate(
        self,
        cards: List[Card],
        pairs: Dict[Value, int],
        by_suit: Dict[str, List[Card]]
    ) -> Union[None, Tuple[Combination, List[Card]]]:
        """
        Проверяет, присутствует ли комбинация, соответствующая валидатору.

        Аргументы:
            cards (List[Card]): Все карты руки и стола (общий пул).
            pairs (Dict[Value, int]): Словарь с количеством карт каждого достоинства
                (предварительно вычисленный для ускорения).
            by_suit (Dict[str, List[Card]]): Карты, сгруппированные по мастям
                (ключ – название масти, значение – список карт этой масти).

        Возвращает:
            Union[None, Tuple[Combination, List[Card]]]:
                - None, если комбинация не обнаружена.
                - Кортеж (Combination, List[Card]), где Combination – тип комбинации,
                  List[Card] – лучшие пять карт, образующих эту комбинацию
                  (отсортированы от старшей к младшей).
        """
        pass


class RoyalFlushValidator(HandValidator):
    """
    Валидатор для комбинации 'Роял-флеш' (Royal Flush).

    Роял-флеш – это стрит-флеш от десятки до туза одной масти.
    Комбинация является самой старшей в покере.
    """
    def validate(self, cards: List[Card], pairs: Dict, by_suit: Dict) -> Union[None, Tuple[Combination, List[Card]]]:
        """
        Проверяет, присутствует ли роял-флеш в переданных картах.
        Возвращает:
            Кортеж (Combination.ROYAL_FLUSH, список карт) при обнаружении,
            иначе None.
        """
        royal_values = {10, 11, 12, 13, 14}
        for suit_cards in by_suit.values():
            if len(suit_cards) < 5:
                continue
            values = {card.value.value for card in suit_cards}
            if royal_values.issubset(values):
                royal_cards = [c for c in suit_cards if c.value.value in royal_values]
                royal_cards.sort(key=lambda c: c.value.value, reverse=True)
                return (Combination.ROYAL_FLUSH, royal_cards[:5])
        return None


class StraightFlushValidator(HandValidator):
    """
    Валидатор для комбинации 'Стрит-флеш' (Straight Flush).

    Стрит-флеш – это пять последовательных карт одной масти.
    Учитывается также 'колесо' (A,2,3,4,5) – самый низкий стрит-флеш.
    """
    def validate(self, cards: List[Card], pairs: Dict, by_suit: Dict) -> Union[None, Tuple[Combination, List[Card]]]:
        """
        Проверяет, присутствует ли стрит-флеш в переданных картах.
        Возвращает:
            Кортеж (Combination.STRAIGHT_FLUSH, список карт) при обнаружении,
            иначе None.
        """
        for suit_cards in by_suit.values():
            if len(suit_cards) < 5:
                continue
            values = sorted(set(c.value.value for c in suit_cards))
            # Проверить стрит-флеш-колесо (A,2,3,4,5)
            if set(values) & {2, 3, 4, 5, 14} == {2, 3, 4, 5, 14}:
                # Найти реальные карты: A,5,4,3,2 этой масти
                wheel_vals = {14, 2, 3, 4, 5}
                wheel_cards = [c for c in suit_cards if c.value.value in wheel_vals]
                wheel_cards.sort(key=lambda c: (c.value.value == 14, c.value.value), reverse=False)
                # Но возвращаем отсортированными по убыванию: 5,4,3,2,A → туз считается низким, поэтому возвращаем [5,4,3,2,A] как есть?
                # Соглашение: сортировать от старшей к младшей, туз низкий → [5,4,3,2,A]
                wheel_cards.sort(key=lambda c: (c.value.value == 14, c.value.value), reverse=True)
                # Теперь туз будет последним
                return (Combination.STRAIGHT_FLUSH, wheel_cards[:5])

            # Поиск обычного стрита
            for i in range(len(values) - 4):
                if all(values[i + j] == values[i] + j for j in range(5)):
                    high_val = values[i + 4]
                    # Собрать по одной карте каждого значения от старшего к младшему
                    straight_cards = []
                    for val in range(high_val, high_val - 5, -1):
                        for c in suit_cards:
                            if c.value.value == val and c not in straight_cards:
                                straight_cards.append(c)
                                break
                    return (Combination.STRAIGHT_FLUSH, straight_cards)
        return None


class FourOfAKindValidator(HandValidator):
    """
    Валидатор для комбинации 'Каре' (Four of a Kind).

    Каре – четыре карты одного достоинства.
    Пятая карта (кикер) используется для определения силы при одинаковом каре.
    """
    def validate(self, cards: List[Card], pairs: Dict, by_suit: Dict) -> Union[None, Tuple[Combination, List[Card]]]:
        """
        Проверяет, присутствует ли каре в переданных картах.
        Возвращает:
            Кортеж (Combination.FOUR_OF_A_KIND, список карт) при обнаружении,
            иначе None.
        """
        fours = [v for v, cnt in pairs.items() if cnt == 4]
        if not fours:
            return None
        value = max(fours, key=lambda v: v.value)
        four_cards = [c for c in cards if c.value == value]
        kickers = [c for c in cards if c.value != value]
        kickers.sort(key=lambda c: c.value.value, reverse=True)
        best = four_cards + kickers[:1]
        best.sort(key=lambda c: c.value.value, reverse=True)
        return (Combination.FOUR_OF_A_KIND, best[:5])


class FullHouseValidator(HandValidator):
    """
    Валидатор для комбинации 'Фулл-хаус' (Full House).

    Фулл-хаус – три карты одного достоинства и две карты другого достоинства.
    При сравнении фулл-хаусов сначала сравнивается тройка, затем пара.
    """
    def validate(self, cards: List[Card], pairs: Dict, by_suit: Dict) -> Union[None, Tuple[Combination, List[Card]]]:
        """
        Проверяет, присутствует ли фулл-хаус в переданных картах.
        Возвращает:
            Кортеж (Combination.FULL_HOUSE, список карт) при обнаружении,
            иначе None.
        """
        threes = [v for v, cnt in pairs.items() if cnt >= 3]
        twos = [v for v, cnt in pairs.items() if cnt >= 2]
        if len(threes) == 0 or len([v for v in twos if v != threes[0]]) == 0:
            return None
        top_three = max(threes, key=lambda v: v.value)
        other_twos = [v for v in twos if v != top_three]
        if not other_twos:
            return None
        top_two = max(other_twos, key=lambda v: v.value)
        three_cards = sorted([c for c in cards if c.value == top_three], key=lambda c: c.value.value, reverse=True)[:3]
        two_cards = sorted([c for c in cards if c.value == top_two], key=lambda c: c.value.value, reverse=True)[:2]
        return (Combination.FULL_HOUSE, three_cards + two_cards)


class FlushValidator(HandValidator):
    """
    Валидатор для комбинации 'Флеш' (Flush).

    Флеш – пять карт одной масти.
    При сравнении флешей сравниваются старшие карты по убыванию.
    """
    def validate(self, cards: List[Card], pairs: Dict, by_suit: Dict) -> Union[None, Tuple[Combination, List[Card]]]:
        """
        Проверяет, присутствует ли флеш в переданных картах.
        Возвращает:
            Кортеж (Combination.FLUSH, список карт) при обнаружении,
            иначе None.
        """
        for suit_cards in by_suit.values():
            if len(suit_cards) >= 5:
                sorted_flush = sorted(suit_cards, key=lambda c: c.value.value, reverse=True)
                return (Combination.FLUSH, sorted_flush[:5])
        return None


class StraightValidator(HandValidator):
    """
    Валидатор для комбинации 'Стрит' (Straight).

    Стрит – пять последовательных карт разных мастей.
    Учитывается 'колесо' (A,2,3,4,5) – самый низкий стрит.
    """
    def validate(self, cards: List[Card], pairs: Dict, by_suit: Dict) -> Union[None, Tuple[Combination, List[Card]]]:
        """
        Проверяет, присутствует ли стрит в переданных картах.
        Возвращает:
            Кортеж (Combination.STRAIGHT, список карт) при обнаружении,
            иначе None.
        """
        values = sorted(set(c.value.value for c in cards))
        # Колесо
        if {2, 3, 4, 5, 14}.issubset(values):
            # Найти A,5,4,3,2
            wheel_cards = [c for c in cards if c.value.value in {14, 2, 3, 4, 5}]
            wheel_cards.sort(key=lambda c: (c.value.value == 14, c.value.value), reverse=True)
            return (Combination.STRAIGHT, wheel_cards[:5])
        # Обычный стрит
        for i in range(len(values) - 4):
            if all(values[i + j] == values[i] + j for j in range(5)):
                high_val = values[i + 4]
                straight_cards = []
                for val in range(high_val, high_val - 5, -1):
                    for c in cards:
                        if c.value.value == val and c not in straight_cards:
                            straight_cards.append(c)
                            break
                return (Combination.STRAIGHT, straight_cards)
        return None


class ThreeOfAKindValidator(HandValidator):
    """
    Валидатор для комбинации 'Тройка' (Three of a Kind).

    Тройка – три карты одного достоинства.
    Две дополнительные карты (кикеры) используются для определения силы при одинаковых тройках.
    """
    def validate(self, cards: List[Card], pairs: Dict, by_suit: Dict) -> Union[None, Tuple[Combination, List[Card]]]:
        """
        Проверяет, присутствует ли тройка в переданных картах.
        Возвращает:
            Кортеж (Combination.THREE_OF_A_KIND, список карт) при обнаружении,
            иначе None.
        """
        threes = [v for v, cnt in pairs.items() if cnt >= 3]
        if not threes:
            return None
        value = max(threes, key=lambda v: v.value)
        three_cards = [c for c in cards if c.value == value]
        three_cards.sort(key=lambda c: c.value.value, reverse=True)
        three_cards = three_cards[:3]
        kickers = [c for c in cards if c.value != value]
        kickers.sort(key=lambda c: c.value.value, reverse=True)
        return (Combination.THREE_OF_A_KIND, three_cards + kickers[:2])


class TwoPairsValidator(HandValidator):
    """
    Валидатор для комбинации 'Две пары' (Two Pairs).

    Две пары – два различных достоинства, каждое из которых образует пару.
    Пятая карта (кикер) используется для определения силы при одинаковых парах.
    """
    def validate(self, cards: List[Card], pairs: Dict, by_suit: Dict) -> Union[None, Tuple[Combination, List[Card]]]:
        """
        Проверяет, присутствуют ли две пары в переданных картах.
        Возвращает:
            Кортеж (Combination.TWO_PAIRS, список карт) при обнаружении,
            иначе None.
        """
        pair_ranks = [v for v, cnt in pairs.items() if cnt >= 2]
        if len(pair_ranks) < 2:
            return None
        pair_ranks.sort(key=lambda v: v.value, reverse=True)
        first, second = pair_ranks[0], pair_ranks[1]
        first_cards = sorted([c for c in cards if c.value == first], key=lambda c: c.value.value, reverse=True)[:2]
        second_cards = sorted([c for c in cards if c.value == second], key=lambda c: c.value.value, reverse=True)[:2]
        kicker = [c for c in cards if c.value not in (first, second)]
        kicker.sort(key=lambda c: c.value.value, reverse=True)
        kicker = kicker[:1] if kicker else []
        return (Combination.TWO_PAIRS, first_cards + second_cards + kicker)


class OnePairValidator(HandValidator):
    """
    Валидатор для комбинации 'Одна пара' (One Pair).

    Одна пара – два карты одного достоинства.
    Три дополнительные карты (кикеры) используются для определения силы при одинаковых парах.
    """
    def validate(self, cards: List[Card], pairs: Dict, by_suit: Dict) -> Union[None, Tuple[Combination, List[Card]]]:
        """
        Проверяет, присутствует ли одна пара в переданных картах.
        Возвращает:
            Кортеж (Combination.ONE_PAIR, список карт) при обнаружении,
            иначе None.
        """
        pair_ranks = [v for v, cnt in pairs.items() if cnt >= 2]
        if not pair_ranks:
            return None
        value = max(pair_ranks, key=lambda v: v.value)
        pair_cards = sorted([c for c in cards if c.value == value], key=lambda c: c.value.value, reverse=True)[:2]
        kickers = [c for c in cards if c.value != value]
        kickers.sort(key=lambda c: c.value.value, reverse=True)
        return (Combination.ONE_PAIR, pair_cards + kickers[:3])


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

    def evaluate_hand(self, cards: List[Card]) -> HandEvaluationResult:
        """
        Оценивает руку, используя предварительную обработку.
        """
        # Предобработка
        pairs = self.find_pairs(cards)
        by_suit = defaultdict(list)
        for card in cards:
            by_suit[card.suit].append(card)

        # Сортируем все карты один раз
        sorted_cards = sorted(cards, key=lambda c: c.value.value, reverse=True)

        # Проверяем каждый валидатор
        for validator in self.__validators:
            result = validator.validate(cards, pairs, by_suit)
            if result:
                return HandEvaluationResult(combination=result[0], cards=result[1])

        return HandEvaluationResult(Combination.HIGH_CARD, sorted_cards[:5])


    def get_combination_name(self, rank: int) -> str:
        """Возвращает название комбинации по её рангу."""
        return Combination(rank).name.replace('_', ' ').title()

    @staticmethod
    def is_straight(cards: List[Card]) -> bool:
        """Проверяет, образуют ли карты стрит."""
        values = sorted(set(c.value.value for c in cards))
        if {2, 3, 4, 5, 14}.issubset(values):
            return True
        for i in range(len(values) - 4):
            if all(values[i + j] == values[i] + j for j in range(5)):
                return True
        return False

    @staticmethod
    def is_flush(cards: List[Card]) -> bool:
        """Проверяет, образуют ли карты флеш."""
        suit_count = defaultdict(int)
        for card in cards:
            suit_count[card.suit] += 1
        return max(suit_count.values(), default=0) >= 5

    @staticmethod
    def find_pairs(cards: List[Card]) -> Dict[Value, int]:
        """Находит пары, триплеты и каре в списке карт."""
        cd_dict = {}
        for card in cards:
            cd_dict[card.value] = cd_dict.get(card.value, 0) + 1
        return {key: val for key, val in cd_dict.items() if val > 1}
