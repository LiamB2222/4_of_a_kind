import random
from typing import List, Optional
from src.game.Deck import Card
from src.game.Hand_evaluation import HandEvaluator, HandRank
from src.game.Game import Player

class PokerAI(Player):
    def __init__(self, name: str, initial_chips: int = 1000, strategy: str = 'conservative'):
        super().__init__(name, initial_chips)
        self.strategy = strategy
    
    def decide_action(self, community_cards: List[Card], current_bet: int) -> str:
        full_hand = self.hand + community_cards
        hand_eval = HandEvaluator.evaluate_hand(full_hand)
        
        hand_rank = hand_eval['rank']
        
        if self.strategy == 'aggressive':
            return self._aggressive_strategy(hand_rank, current_bet)
        elif self.strategy == 'conservative':
            return self._conservative_strategy(hand_rank, current_bet)
        else:
            return self._balanced_strategy(hand_rank, current_bet)
    
    # Aggressive strategy
    def _aggressive_strategy(self, hand_rank: HandRank, current_bet: int) -> str:
        if hand_rank.value >= HandRank.THREE_OF_A_KIND.value:
            return 'raise'
        elif hand_rank.value >= HandRank.PAIR.value:
            return 'raise' if random.random() > 0.5 else 'call'
        elif current_bet > self.chips * 0.2:
            return 'fold'
        else:
            return 'call'
    
    # conservative strategy only strong hands
    def _conservative_strategy(self, hand_rank: HandRank, current_bet: int) -> str:
        if hand_rank.value >= HandRank.STRAIGHT.value:
            return 'raise'
        elif hand_rank.value >= HandRank.THREE_OF_A_KIND.value:
            return 'call'
        elif current_bet > self.chips * 0.1:
            return 'fold'
        else:
            return 'call'
    
    # adding balanced strategy mix of aggressive and conservative
    def _balanced_strategy(self, hand_rank: HandRank, current_bet: int) -> str:
        if hand_rank.value >= HandRank.FULL_HOUSE.value:
            return 'raise'
        elif hand_rank.value >= HandRank.PAIR.value:
            return 'raise' if random.random() < 0.3 else 'call'
        elif current_bet > self.chips * 0.15:
            return 'fold'
        else:
            return 'call'
    
    def place_bet(self, current_bet: int) -> Optional[int]:
        action = self.decide_action([], current_bet)
        
        if action == 'fold':
            return None
        
        base_bet = current_bet * 1.5 if action == 'raise' else current_bet
        
        bet_amount = min(base_bet, self.chips)
        
        return int(bet_amount)