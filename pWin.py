from treys import (
    Evaluator as TreysEvaluator,
    Deck as TreysDeck,
    Card as TreysCard
)

hand_evaluator = TreysEvaluator()


def calculate_win_probability(hand, board, num_players):
    num_simulations = 10000

    simulated_wins = simulate_game(
        hand,
        board,
        num_players,
        num_simulations
    )

    return simulated_wins / num_simulations


def simulate_game(hand, board, num_players, num_simulations):
    deck = TreysDeck()
    wins = 0

    for i in range(num_simulations):
        setup = sim_new_setup(hand, deck, board, num_players)
        simulated_board = setup['simulated_board']
        hands_of_all_opponents = setup['hands_of_all_opponents']

        if i_won_the_hand(hand, hands_of_all_opponents, simulated_board, num_players):
            wins += 1

    print(f'Wins: {wins}')
    return wins


def sim_new_setup(hand, deck, board, num_players):
    deck.shuffle()

    # remove hand and existing board cards from deck
    for card in hand + board:
        deck.cards.remove(card)

    # generate hands of all opponents
    hands_of_all_opponents = []
    for player in range(num_players - 1):
        hand_of_opponent = deck.draw(2)
        hands_of_all_opponents.append(hand_of_opponent)

    # add missing cards to get a full board
    num_cards_missing_from_board = 5 - len(board)
    new_board_cards = deck.draw(num_cards_missing_from_board)
    simulated_board = []
    for card in board + new_board_cards:
        simulated_board.append(card)

    """
    print("Hand: ")
    TreysCard.print_pretty_cards(hand)

    print("Board: ")
    TreysCard.print_pretty_cards(simulated_board)

    for hand in hands_of_all_opponents:
        print("Opp: ")
        TreysCard.print_pretty_cards(hand)  
    #"""

    return {
        'simulated_board': simulated_board,
        'hands_of_all_opponents': hands_of_all_opponents,
    }


def i_won_the_hand(my_hand, opponents_hands, board, num_players):
    my_hand_score = hand_evaluator.evaluate(hand=my_hand, board=board)
    opponents_hands_score = []

    for player in range(num_players - 1):
        hand_score = hand_evaluator.evaluate(hand=opponents_hands[player], board=board)
        if hand_score < my_hand_score:
            return False
        opponents_hands_score.append(hand_score)

    best_hand_of_opponents = min(opponents_hands_score)

    return my_hand_score < best_hand_of_opponents
