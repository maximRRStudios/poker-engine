import pytest
from poker_engine.card import Card
from poker_engine.constants import Suit, Value

@pytest.fixture
def example_card():
    return Card(Suit.HEARTS, Value.KING)

def test_initialization(example_card):
    assert example_card.suit == Suit.HEARTS
    assert example_card.value == Value.KING

def test_string_representation():
    card = Card(Suit.SPADES, Value.ACE)
    expected_str = "ACE of SPADES"
    assert str(card) == expected_str

def test_equality():
    card1 = Card(Suit.CLUBS, Value.NINE)
    card2 = Card(Suit.DIAMONDS, Value.NINE)
    assert card1 == card2  # Должны быть равны по достоинству

def test_less_than_comparison():
    card1 = Card(Suit.HEARTS, Value.FOUR)
    card2 = Card(Suit.CLUBS, Value.SEVEN)
    assert card1 < card2  # Первая карта должна быть меньше второй

def test_greater_than_comparison():
    card1 = Card(Suit.SPADES, Value.JACK)
    card2 = Card(Suit.HEARTS, Value.TWO)
    assert card1 > card2  # Первая карта должна быть больше второй

def test_unsupported_comparisons():
    card = Card(Suit.HEARTS, Value.EIGHT)
    non_card_object = "String"
    with pytest.raises(TypeError):
        card < non_card_object

def test_hashability():
    card_set = {Card(Suit.CLUBS, Value.NINE)}
    assert Card(Suit.CLUBS, Value.NINE) in card_set
