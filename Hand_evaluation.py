from enum import Enum, auto
from typing import List, Dict
from Deck import Card

# lowest to highest rank
class HandRank(Enum):
    HIGH_CARD = 1
    PAIR = 2
    TWO_PAIR = 3
    THREE_OF_A_KIND = 4
    STRAIGHT = 5
    FLUSH = 6
    FULL_HOUSE = 7
    FOUR_OF_A_KIND = 8
    STRAIGHT_FLUSH = 9
    ROYAL_FLUSH = 10

class HandEvaluator:
    def evaluate_hand(cards: List[Card]) -> Dict[str, any]:
        #Sort cards by rank in descending order
        sorted_cards = sorted(cards, key=lambda x: x.rank.value, reverse=True)
        #Check for flush
        is_flush = len(set(card.suit for card in cards)) == 1
        #Check for straight
        ranks = [card.rank.value for card in sorted_cards]
        is_straight = (len(set(ranks)) == 5) and (max(ranks) - min(ranks) == 4)
        #Analyze card frequencies
        rank_counts = {}
        for card in cards:
            if card.rank not in rank_counts:
                rank_counts[card.rank] = 0
            rank_counts[card.rank] += 1
        
        #Determine hand rank
        if is_straight and is_flush:
            if set(ranks) == {10, 11, 12, 13, 14}:
                return {
                    'rank': HandRank.ROYAL_FLUSH,
                    'primary_value': 14
                }
            return {
                'rank': HandRank.STRAIGHT_FLUSH,
                'primary_value': max(ranks)
            }
        
        # Four of a kind
        if 4 in rank_counts.values():
            four_rank = [r for r, count in rank_counts.items() if count == 4][0]
            return {
                'rank': HandRank.FOUR_OF_A_KIND,
                'primary_value': four_rank.value
            }
        
        # Full house
        if 3 in rank_counts.values() and 2 in rank_counts.values():
            three_rank = [r for r, count in rank_counts.items() if count == 3][0]
            two_rank = [r for r, count in rank_counts.items() if count == 2][0]
            return {
                'rank': HandRank.FULL_HOUSE,
                'primary_value': three_rank.value,
                'secondary_value': two_rank.value
            }
        
        # Flush
        if is_flush:
            return {
                'rank': HandRank.FLUSH,
                'primary_value': ranks
            }
        
        # Straight
        if is_straight:
            return {
                'rank': HandRank.STRAIGHT,
                'primary_value': max(ranks)
            }
        
        # Three of a kind
        if 3 in rank_counts.values():
            three_rank = [r for r, count in rank_counts.items() if count == 3][0]
            return {
                'rank': HandRank.THREE_OF_A_KIND,
                'primary_value': three_rank.value
            }
        
        # Two pair
        pairs = [r for r, count in rank_counts.items() if count == 2]
        if len(pairs) == 2:
            return {
                'rank': HandRank.TWO_PAIR,
                'primary_value': max(p.value for p in pairs),
                'secondary_value': min(p.value for p in pairs)
            }
        
        # One pair
        if 2 in rank_counts.values():
            pair_rank = [r for r, count in rank_counts.items() if count == 2][0]
            return {
                'rank': HandRank.PAIR,
                'primary_value': pair_rank.value
            }
        
        # High card
        return {
            'rank': HandRank.HIGH_CARD,
            'primary_value': ranks
        }

    def compare_hands(hand1: List[Card], hand2: List[Card]) -> int:
        eval1 = HandEvaluator.evaluate_hand(hand1)
        eval2 = HandEvaluator.evaluate_hand(hand2)
        
        if eval1['rank'].value > eval2['rank'].value:
            return 1
        elif eval1['rank'].value < eval2['rank'].value:
            return -1
        
        # If ranks are the same, compare primary values
        if isinstance(eval1['primary_value'], list):
            # For hands like flush or high card, compare each card
            for card1, card2 in zip(sorted(eval1['primary_value'], reverse=True), 
                                    sorted(eval2['primary_value'], reverse=True)):
                if card1 > card2:
                    return 1
                elif card1 < card2:
                    return -1
            return 0
        
        if eval1['primary_value'] > eval2['primary_value']:
            return 1
        elif eval1['primary_value'] < eval2['primary_value']:
            return -1
        
        # If primary values are the same, check secondary values if they exist
        if 'secondary_value' in eval1 and 'secondary_value' in eval2:
            if eval1['secondary_value'] > eval2['secondary_value']:
                return 1
            elif eval1['secondary_value'] < eval2['secondary_value']:
                return -1
        
        return 0