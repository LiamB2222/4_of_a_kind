from typing import List, Dict
from .Deck import Deck, Card
from .Hand_evaluation import HandEvaluator, HandRank
from enum import Enum
from AI.pWin import calculate_win_probability


class Player:
    def __init__(self, name: str, game: 'PokerGame', initial_chips: int = 1000, ):
        self.name = name
        self.chips = initial_chips
        self.hand: List[Card] = []
        self.current_bet: int = 0
        self.folded: bool = False
        self.game: 'PokerGame'
        
    
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
    
   
class Play (Enum) :
    '''created as output for our decide Play function'''
    FOLD = 0
    CALL = 1
    RAISE = 2 
    CHECK = 3
    ALL_IN = 4
    BET = 5

class AI_Player(Player) :
    '''class for the actual AI agent behavior functions should be put here 
    as well as infromation about the AI itself'''
    def __init__(self, name: str, initial_chips: int = 10000):
        super().__init__(name, initial_chips)
        self.turn_pot_percentage_targets[0,0.25,0.5,1]          # This determines how the AI will become more agressive as turns progress 
                                                                # specifically will track a target ideal amount to have bet by the end of the round 
                                                                # based on its current probability of winning 
                                                                # the numbers represent how much of that ideal amount the AI will bet on bets on turn 1,2, ect
        
        self.max_risk_factor = initial_chips * self.game.number_of_players  # should be set to the maximum amount the AI will aim to drive the pot to in a single round (thats round not turn)(may be driven higher to save sunk costs)
        self.persistance_factor = 0.5             # how much the AI will be willing to persue sunk costs even if the odds are not in its favor (scales with )


    def my_win_probability(self):
        '''wrapper for calculate_win_probability function but automatically uses paramaters for this player'''
        return calculate_win_probability(self.hand,self.game.community_cards,self.game.number_of_players)

    def confidence(self):
        if confidence := (self.my_win_probability - 0.5) * 2 > 0:
            return confidence
        else:
            return 0.0

    def Play_Turn(self) : 
        '''function to play out the turn will return 
        a tuple with the decided play and the amount 
        to add to the pot if applicable'''
        pass    

   
    def calc_target_final_pot(self, confidence) :
        '''function to calculate the ideal pot size gien the current p_win 
            for now will just throw something out will adjust later with testing
            Will need to figure out how this works with multiple other players if we scale to that
        '''
        return 
    
    def Decide_Play (self,confidence,call_value):
        '''Will return play type'''
        ideal_pot = self.max_risk_factor * confidence * self.turn_pot_percentage_targets[self.game.turn_number]
        
        if self.game.current_pot > ideal_pot:
            if call_value ==  0:
                return Play.CALL
            else:
                if call_value > self.max_persistance_factor :
                    return Play.FOLD

             
    def Decide_Bet (PLAY, current_pot = 0, p_win = 0.5, call_value = 0,ideal_pot = 0) :
        '''When raise or bet is selected play decide how much to bet if given call will simply return call_value'''
        if PLAY == Play.FOLD or PLAY == Play.CHECK:
            return 0
        
        if PLAY == Play.CALL:
            return call_value
        
        
