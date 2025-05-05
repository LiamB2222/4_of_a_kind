import random
from enum import Enum, auto
from treys import Card as TreyCard
class Suit(Enum):
    HEARTS = 'h'
    DIAMONDS = 'd'
    CLUBS = 'c'
    SPADES = 's'

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


def To_Trays(Card :Card = Card(Rank.TWO,Suit.SPADES)) -> TreyCard:
        '''Convert the card to a format compatible with the Treys library'''
        rank = ''
        if Card.rank == Rank.ACE:
            rank = 'A'
        elif Card.rank == Rank.TWO:
            rank = '2'
        elif Card.rank == Rank.THREE:
            rank = '3'
        elif Card.rank == Rank.FOUR:
            rank = '4'
        elif Card.rank == Rank.FIVE:
            rank = '5'
        elif Card.rank == Rank.SIX:
            rank = '6'
        elif Card.rank == Rank.SEVEN:
            rank = '7'
        elif Card.rank == Rank.EIGHT:
            rank = '8'
        elif Card.rank == Rank.NINE:
            rank = '9'
        elif Card.rank == Rank.TEN:
            rank = 'T'
        elif Card.rank == Rank.JACK:
            rank = 'J'
        elif Card.rank == Rank.QUEEN:
            rank = 'Q'
        elif Card.rank == Rank.KING:
            rank = 'K'
        else:
            raise ValueError("Invalid rank")
        
        return TreyCard.new(str(Card.rank.value) + Card.suit.value)