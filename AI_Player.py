
from Player import Player
from Game import Game
from enum import Enum
from AI.pWin import calculate_win_probability


class Play (Enum) :
    '''created as output for our decide Play function'''
    FOLD = 'fold'
    CALL = 'call'
    RAISE = 'raise'
    CHECK = 'check'
    BET = 'bet'

class AI_Player(Player) :
    '''class for the actual AI agent behavior functions should be put here 
    as well as infromation about the AI itself'''
    def __init__(self, name: str, initial_chips: int = 10000):
        super().__init__(name, initial_chips)
        self.turn_pot_percentage_targets[0,0.25,0.5,1]          # This determines how the AI will become more agressive as turns progress 
                                                                # specifically will track a target ideal amount to have bet by the end of the round 
                                                                # based on its current probability of winning 
                                                                # the numbers represent how much of that ideal amount the AI will bet on bets on turn 1,2, ect

        self.risk_factor = 0.1                 # this is the risk factor for the AI and will be used to determine how much it is willing to bet based on its current win probability
        self.max_bet = initial_chips * self.game.number_of_players * self.risk_factor # should be set to the maximum amount the AI will aim to drive the pot to in a single round (thats round not turn)(may be driven higher to save sunk costs)
        self.persistance_factor = 0.5             # how much the AI will be willing to persue sunk costs even if the odds are not in its favor (scales with )


    def my_win_probability(self):
        '''wrapper for calculate_win_probability function but automatically uses paramaters for this player'''
        return calculate_win_probability(self.hand,self.game.community_cards,self.game.number_of_players)

    def confidence(self):
        if confidence := (self.my_win_probability - 0.5) * 2 > 0:
            return confidence
        else:
            return 0.0
    
    def Decide_Play (self,confidence,call_minimum):
        '''Will return play type'''
        ideal_pot = self.max_bet * confidence * self.turn_pot_percentage_targets[self.game.turn_number]
        
        if self.game.current_pot + call_minimum >= ideal_pot:
            if call_minimum ==  0:
                return Play.CHECK
            else:
                if call_minimum > (self.game.current_pot - ideal_pot) * self.persistance_factor :
                    return Play.FOLD
                else:
                    return Play.CALL
        
        if self.game.current_pot + call_minimum < ideal_pot:
            if call_minimum == 0:
                return Play.BET
            else:
                return Play.RAISE
            
            
                


    def Take_Turn (self, current_pot = 0, p_win = 0.5, call_value = 0,ideal_pot = 0) :
        '''function to play out the turn might have to work on this more with poleth later '''


        play = self.Decide_Play(self.my_win_probability(),call_value)
        call_value 

        if play == Play.FOLD:
            self.fold()
        
        if play == Play.CHECK:
            self.bet(0)
            
        if play == Play.CALL:
            self.bet(call_value)
            return Play.CALL

    