import random
from enum import Enum, auto

class Suit(Enum):
    HEARTS = auto()
    DIAMONDS = auto()
    CLUBS = auto()
    SPADES = auto()

class Rank(Enum):
    ACE = 14
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

class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
    def __repr__(self):
        return f"{self.rank.name} of {self.suit.name}"
    
class Deck:
    def __init__(self):
        self.cards = [
            Card(suit, rank) 
            for suit in Suit 
            for rank in Rank
        ]
        self.shuffle()
    
    def shuffle(self):
        random.shuffle(self.cards)
    
    def draw(self):
        if not self.cards:
            raise ValueError("No cards left in the deck")
        return self.cards.pop()
    
    def reset(self):
        self.__init__()