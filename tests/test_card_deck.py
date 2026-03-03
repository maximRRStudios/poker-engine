import pytest
from poker_engine.card_deck import CardDeck
from poker_engine.card import Card
from poker_engine.constants import Suit, Value

@pytest.fixture
def fresh_deck():
    return CardDeck()

def test_initial_deck_has_52_cards(fresh_deck):
    assert len(fresh_deck) == 52

def test_draw_card_reduces_deck_size(fresh_deck):
    initial_length = len(fresh_deck)
    fresh_deck.draw_card()
    assert len(fresh_deck) == initial_length - 1

def test_draw_card_returns_correct_type(fresh_deck):
    drawn_card = fresh_deck.draw_card()
    assert isinstance(drawn_card, Card)

def test_reset_restores_full_deck(fresh_deck):
    # Сначала заберём несколько карт
    for _ in range(10):
        fresh_deck.draw_card()
    
    # Проверим, что размер уменьшился
    assert len(fresh_deck) == 42
    
    # Восстанавливаем колоду
    fresh_deck.reset()
    
    # Проверим, что восстановилось 52 карты
    assert len(fresh_deck) == 52

def test_shuffle_changes_order(fresh_deck):
    original_order = fresh_deck.cards.copy()
    fresh_deck.shuffle()
    shuffled_order = fresh_deck.cards
    
    # Проверим, что порядок изменился
    assert original_order != shuffled_order

def test_empty_deck_raises_error(fresh_deck):
    # Заберем все карты из колоды
    for _ in range(52):
        fresh_deck.draw_card()
    
    # Попытка забрать карту из пустой колоды должна бросать ошибку
    with pytest.raises(IndexError):
        fresh_deck.draw_card()

def test_deck_contains_unique_cards(fresh_deck):
    # Проверим, что все карты уникальные
    unique_cards = set(fresh_deck.cards)
    assert len(unique_cards) == 52

def test_deck_contains_all_values_and_suits(fresh_deck):
    # Проверим, что в колоде присутствуют все масти и достоинства
    suits_in_deck = {card.suit for card in fresh_deck.cards}
    values_in_deck = {card.value for card in fresh_deck.cards}
    
    assert suits_in_deck == set(Suit)
    assert values_in_deck == set(Value)