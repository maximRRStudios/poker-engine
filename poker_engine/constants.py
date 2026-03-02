"""
Константы
"""
from enum import Enum

class Suit(Enum):
    """Масти"""
    
    HEARTS = 1
    DIAMONDS = 2
    CLUBS = 3
    SPADES = 4


class Value(Enum):
    """Значения карт"""
    
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = 11
    QUEEN = 12
    KING = 13
    ACE = 14
