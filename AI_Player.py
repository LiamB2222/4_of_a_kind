
from Player import Player
from enum import Enum
from pWin import calculate_win_probability



class AI_Player(Player) :
    '''class for the actual AI agent behavior functions should be put here 
    as well as infromation about the AI itself'''
    def __init__(self, name: str, initial_chips: int = 10000):
        super().__init__(name, initial_chips)
        self.turn_pot_percentage_targets = [0,0.25,0.5,1]          # This determines how the AI will become more agressive as turns progress 
                                                                # specifically will track a target ideal amount to have bet by the end of the round 
                                                                # based on its current probability of winning 
                                                                # the numbers represent how much of that ideal amount the AI will bet on bets on turn 1,2, ect
        self.boldness = 0.1                 # this is the risk factor for the AI and will be used to determine how much it is willing to bet based on its current win probability
        self.max_pot = 0 
        self.persistance_factor = 0.5             # how much the AI will be willing to persue sunk costs even if the odds are not in its favor (scales with )


        # this is the ideal amount the AI wants to have in the pot at the end of the round based on its current win probability and how far into the game it is
        # todo: add function to asses current game state and adjust relvant values (example max pot might go down if we have lost chips)

    def update_max_pot(self):
        '''function to update the max pot value based on the current game state'''
        self.max_pot = self.chips * self.game.number_of_players * self.boldness
        return self.max_pot

    def my_win_probability(self):
        '''wrapper for calculate_win_probability function but automatically uses paramaters for this player'''
        prob = calculate_win_probability(self.hand,self.game.community_cards,self.game.number_of_players)
        return prob

    @property
    def confidence(self):
        confidence = (self.my_win_probability() - 0.5) * 2
        if confidence  > 0:
            return confidence
        else:
            return 0.0
    
    @property
    def ideal_pot(self):
        '''function to determine the ideal pot value based on the current game state'''
        ideal_pot = self.max_pot * self.confidence * self.turn_pot_percentage_targets[self.game.turn_number - 1]
        if ideal_pot < 0:
            return 0
        else: # bassically how likely we are to win * how far in the game are we
            return ideal_pot

    def Decide_Action (self,call_minimum):
        '''Will return play type'''
        self.update_max_pot() # update the max pot value based on the current game state
        ideal_pot_ = self.ideal_pot
        
        if self.game.current_pot + call_minimum >= ideal_pot_:
            if call_minimum ==  0:
                return 'check'
            else:
                if call_minimum > (self.game.current_pot - ideal_pot_) * self.persistance_factor :   #check if can exploit by repatedly betting over max pot
                    return 'fold'
                else:
                    return 'call'
    
        if self.game.current_pot + call_minimum < ideal_pot_:
            if call_minimum == 0:    
                return 'bet'
            else:
                return 'raise'

    def Get_Raise_Amount(self):
        '''function to determine how much to bet based on the current game state'''
        amount = int(self.ideal_pot - self.game.current_pot)
        return amount if amount > 0 else 0






    # currently not used since UI handels it but might be useful later
    # def Place_Bet (self, current_pot = 0, call_value = 0,ideal_pot = 0) :
    #     '''function to play out the turn might have to work on this more with poleth later '''
    #     play = self.Decide_Play(self.my_win_probability(),call_value)


    #     if play == 'fold':
    #         self.fold()
        
    #     if play == 'check':
    #         self.bet(0)
            
    #     if play == 'call':
    #         self.bet(call_value)
    #         return 'call'

    #     if play == 'raise' or 'bet':
    #         self.bet(ideal_pot - current_pot)
    #         return 'raise' if play == 'raise' else 'bet'

    