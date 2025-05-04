from typing import List, Dict
from .Deck import Deck, Card
from .Hand_evaluation import HandEvaluator, HandRank
from .Player import Player

class PokerGame:
    def __init__(self, players: List[str], small_blind: int = 10):
        # Ensure small_blind is an integer
        small_blind = int(small_blind)
        
        self.deck = Deck()
        self.players = [Player(name,game=self) for name in players]
        self.community_cards: List[Card] = []
        self.small_blind = small_blind
        self.current_pot: int = 0
        self.current_player_index: int = 0
        self.number_of_players = len(players)
    
    @property
    def turn_number(self) -> int:
        '''Tracks the turn number based on the number of community cards'''
        if len(self.community_cards) == 0:
            return 1
        elif len(self.community_cards) == 3:
            return 2
        elif len(self.community_cards) == 4:
            return 3
        elif len(self.community_cards) == 5:
            return 4

    def deal_initial_cards(self):
        # Deal 2 cards to each player
        for _ in range(2):
            for player in self.players:
                player.receive_card(self.deck.draw())
    
    def deal_community_cards(self, num_cards: int = 3):
        for _ in range(num_cards):
            self.community_cards.append(self.deck.draw())
    
    # collect the bets from each player
    def collect_bets(self, minimum_bet: int):
        for player in self.players:
            if not player.folded:
                try:
                    bet_amount = player.bet(minimum_bet)
                    self.current_pot += bet_amount
                except ValueError:
                    # Player cannot match the bet, they fold
                    player.fold()
    
    # determine the winner of the game
    def determine_winner(self) -> Player:
        active_players = [p for p in self.players if not p.folded]
        
        if len(active_players) == 1:
            return active_players[0]
        
        # Combine each player's hand with community cards
        player_hands = []
        for player in active_players:
            full_hand = player.hand + self.community_cards
            player_hands.append((player, full_hand))
        
        # Find the winner by comparing hands
        winner = max(player_hands, key=lambda x: HandEvaluator.evaluate_hand(x[1])['rank'].value)
        return winner[0]
    
    # reset the game
    def reset_game(self):
        self.deck = Deck()
        self.community_cards = []
        self.current_pot = 0

        for player in self.players:
            player.reset_hand()
    
   
        
        
