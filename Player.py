from typing import List
from Deck import Card
class Player:
    def __init__(self, name: str, initial_chips: int = 1000, ):
        self.name = name
        self.chips = initial_chips
        self.hand: List[Card] = []
        self.current_bet: int = 0
        self.folded: bool = False
        self.game = None
        
    def set_game(self, game):
        self.game = game
    
    def receive_card(self, card: Card):
        self.hand.append(card)
    
    def bet(self, amount: int):
        # Ensure amount is a whole number (integer)
        if not isinstance(amount, int):
            try:
                amount = int(amount)
            except (ValueError, TypeError):
                raise ValueError("Bet amount must be a whole number")
                
        if amount < 0:
            raise ValueError("Bet amount cannot be negative")
            
        if amount > self.chips:
            raise ValueError("Not enough chips to place this bet")
            
        self.chips -= amount
        self.current_bet += amount
        return amount
    
    def fold(self):
        self.folded = True
    
    def reset_hand(self):
        self.hand = []
        self.current_bet = 0
        self.folded = False