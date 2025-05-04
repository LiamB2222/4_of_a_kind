import os
import sys

# Add the project root to the Python path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

from Game import PokerGame
from Player import Player
from UI import PokerGameUI
from AI_Player import AI_Player

def main():
    # Use the CARD folder in the project directory
    CARD_IMAGES_PATH = os.path.join(BASE_DIR, 'CARD')
    
    # If the images directory doesn't exist, use a default path that will trigger placeholder images
    if not os.path.exists(CARD_IMAGES_PATH):
        print(f"Card images directory not found at {CARD_IMAGES_PATH}")
        print("Using placeholder cards instead")
        CARD_IMAGES_PATH = os.path.join(BASE_DIR, 'non_existent_path')

    # Player setup, added one player and two AI players for testing
    
    players = [
        Player("Liam", initial_chips=1000),
        AI_Player("AI Player 1", initial_chips=1000),
        AI_Player("AI Player 2", initial_chips=1000)
    ]
    game = PokerGame(players)
    


    # I dont think this does much other than set AI strategy if im wrong please let me know otherwise we can remove this
    # Liam

    # Create AI players
    # ai_player1 = PokerAI("AI Player 1", strategy='aggressive')
    # ai_player2 = PokerAI("AI Player 2", strategy='conservative')
    
    # # Replace AI player names with actual AI instances
    # game.players[1] = ai_player1
    # game.players[2] = ai_player2

    ui = PokerGameUI(game, card_image_path=CARD_IMAGES_PATH)
    ui.start_game()

if __name__ == "__main__":
    main()