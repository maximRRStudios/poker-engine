import pytest
from poker_engine.ranker import Ranker
from poker_engine.card import Card
from poker_engine.constants import Suit, Value

@pytest.fixture
def ranker():
    return Ranker()

def test_high_card(ranker):
    """
    Тест на старшую карту
    """
    pass

def test_pair(ranker):
    """
    Тест на пару
    """
    pass

def test_kicker_in_one_pair(ranker):
    """
    Тест на выбор кикера в паре
    """
    pass

def test_two_pairs(ranker):
    """
    Тест на две пары
    """
    pass

def test_two_pairs_with_three_pairs(ranker):
    """
    Тест на две пары с тремя парами
    """
    pass

def test_kicker_selection_in_two_pairs(ranker):
    """
    Тест на выбор кикера в двух парах
    """
    pass

def test_three_of_a_kind(ranker):
    """
    Тест на тройку
    """
    pass

def test_straight(ranker):
    """
    Тест на последовательность
    """
    pass

def test_straight_with_duplicate_values(ranker):
    """
    Тест на последовательность с дублирующимися значениями
    """
    pass

def test_straight_wheel(ranker):
    """
    Тест на стрит начинающийся с туза
    """
    pass

def test_flush(ranker):
    """
    Тест на флеш
    """
    pass

def test_flush_with_more_than_5_cards(ranker):
    """
    Тест на флеш с больше чем 5 картами
    """
    pass

def test_full_house(ranker):
    """
    Тест на фулл хаус
    """
    pass

def test_full_house_with_multiple_threes(ranker):
    """
    Тест на фулл хаус с несколькими тройками
    """
    pass

def test_four_of_a_kind(ranker):
    """
    Тест на четверку
    """
    pass

def test_straight_flush(ranker):
    """
    Тест на последовательность флеш
    """
    pass

def test_straight_flush_wheel(ranker):
    """
    Тест на стрит флеш начинающийся с туза
    """
    pass

def test_royal_flush(ranker):
    """
    Тест на роял флеш
    """
    pass

def test_cards_returned_in_descending_order(ranker):
    """
    Тест на возвращение карт в порядке убывания
    """
    pass
