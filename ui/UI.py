import tkinter as tk
from tkinter import messagebox
import os
import random
from typing import List, Dict
from ai.AI import PokerAI

class PokerGameUI:
    def __init__(self, game, card_image_path: str = 'card_images/'):
        self.game = game
        self.card_image_path = card_image_path
        self.card_images: Dict[str, tk.PhotoImage] = {}
        self.win_count = 0
        self.loss_count = 0
        
        self.root = tk.Tk()
        self.root.title("Texas Hold'em Poker")
        self.root.geometry("1200x800")
        
        self.load_card_images()
        
        self.create_game_board()
        self.create_player_areas()
        self.create_action_buttons()
        self.create_stats_display()
    
    def create_stats_display(self):
        stats_frame = tk.Frame(self.root)
        stats_frame.pack(pady=10)
        
        self.win_label = tk.Label(stats_frame, text="Wins: 0", font=('Arial', 12))
        self.win_label.pack(side=tk.LEFT, padx=10)
        
        self.loss_label = tk.Label(stats_frame, text="Losses: 0", font=('Arial', 12))
        self.loss_label.pack(side=tk.LEFT, padx=10)
    
    def update_stats(self, won: bool):
        if won:
            self.win_count += 1
        else:
            self.loss_count += 1
        
        self.win_label.config(text=f"Wins: {self.win_count}")
        self.loss_label.config(text=f"Losses: {self.loss_count}")
    
    def create_placeholder_image(self, text):
        img = tk.PhotoImage(width=80, height=120)
        
        for y in range(120):
            for x in range(80):
                if x < 2 or x >= 78 or y < 2 or y >= 118:
                    img.put('black', (x, y))
                else:
                    img.put('white', (x, y))
        
        return img
    
    def load_card_images(self):
        print(f"Loading card images from: {self.card_image_path}")
        try:
            card_back_path = os.path.join(self.card_image_path, 'card_back.png')
            print(f"Looking for card back at: {card_back_path}")
            if os.path.exists(card_back_path):
                self.card_back = tk.PhotoImage(file=card_back_path)
                print("Successfully loaded card back image")
            else:
                self.card_back = self.create_placeholder_image("BACK")
                print(f"Warning: Card back image not found at {card_back_path}, using placeholder")
        except tk.TclError as e:
            self.card_back = self.create_placeholder_image("BACK")
            print(f"Warning: Could not load card back image: {e}")
        
        cards_loaded = 0
        cards_missing = 0
        
        for suit in ['HEARTS', 'DIAMONDS', 'CLUBS', 'SPADES']:
            for rank in ['TWO', 'THREE', 'FOUR', 'FIVE', 'SIX', 'SEVEN', 'EIGHT', 
                        'NINE', 'TEN', 'JACK', 'QUEEN', 'KING', 'ACE']:
                try:
                    img_path = os.path.join(self.card_image_path, f'{rank}_of_{suit}.png')
                    if os.path.exists(img_path):
                        self.card_images[f'{rank}_of_{suit}'] = tk.PhotoImage(file=img_path)
                        cards_loaded += 1
                    else:
                        self.card_images[f'{rank}_of_{suit}'] = self.create_placeholder_image(f"{rank[0]}{suit[0]}")
                        print(f"Warning: Card image not found at {img_path}")
                        cards_missing += 1
                except tk.TclError as e:
                    self.card_images[f'{rank}_of_{suit}'] = self.create_placeholder_image(f"{rank[0]}{suit[0]}")
                    print(f"Warning: Could not load image {img_path}: {e}")
                    cards_missing += 1
        
        print(f"Card loading complete: {cards_loaded} cards loaded, {cards_missing} cards using placeholders")
    
    def create_game_board(self):
        self.community_cards_frame = tk.Frame(self.root, bg='dark green')
        self.community_cards_frame.pack(pady=20)
        
        self.community_card_labels = []
        for _ in range(5):
            label = tk.Label(self.community_cards_frame, bg='dark green')
            label.pack(side=tk.LEFT, padx=5)
            self.community_card_labels.append(label)
        
        self.pot_label = tk.Label(self.root, text="Pot: $0", font=('Arial', 16))
        self.pot_label.pack(pady=10)
        
        self.current_player_label = tk.Label(self.root, text="Current Player: None", font=('Arial', 14))
        self.current_player_label.pack(pady=5)
    
    def create_player_areas(self):
        self.players_frame = tk.Frame(self.root)
        self.players_frame.pack(expand=True, fill=tk.BOTH)
        
        self.player_hand_labels = []
        self.player_chip_labels = []
        self.player_frames = []
        self.thinking_labels = []  # For AI thinking animation
        
        for i, player in enumerate(self.game.players):
            player_frame = tk.Frame(self.players_frame, padx=10, pady=10)
            player_frame.pack(side=tk.LEFT, expand=True, padx=10)
            self.player_frames.append(player_frame)
            
            name_label = tk.Label(player_frame, text=player.name, font=('Arial', 12, 'bold'))
            name_label.pack()
            
            hand_frame = tk.Frame(player_frame)
            hand_frame.pack(pady=5)
            
            player_hand_labels = []
            for _ in range(2):  
                label = tk.Label(hand_frame)
                label.pack(side=tk.LEFT, padx=2)
                player_hand_labels.append(label)
            
            chip_label = tk.Label(player_frame, text=f"Chips: ${player.chips}", font=('Arial', 12))
            chip_label.pack()
            
            # Add thinking label for AI players
            thinking_label = tk.Label(player_frame, text="", font=('Arial', 10))
            thinking_label.pack()
            self.thinking_labels.append(thinking_label)
            
            self.player_hand_labels.append(player_hand_labels)
            self.player_chip_labels.append(chip_label)

    def create_action_buttons(self):
        action_frame = tk.Frame(self.root)
        action_frame.pack(pady=20)
        
        self.fold_button = tk.Button(action_frame, text="Fold", command=self.handle_fold)
        self.fold_button.pack(side=tk.LEFT, padx=5)
        
        self.call_button = tk.Button(action_frame, text="Call", command=self.handle_call)
        self.call_button.pack(side=tk.LEFT, padx=5)
        
        self.raise_button = tk.Button(action_frame, text="Raise", command=self.handle_raise)
        self.raise_button.pack(side=tk.LEFT, padx=5)
        
        self.raise_entry = tk.Entry(action_frame, width=10)
        self.raise_entry.pack(side=tk.LEFT, padx=5)
    
    def update_ui(self):
        for i in range(5):
            if i < len(self.game.community_cards):
                card = self.game.community_cards[i]
                card_key = f"{card.rank.name}_of_{card.suit.name}"
                self.community_card_labels[i].config(image=self.card_images.get(card_key, self.card_back))
            else:
                self.community_card_labels[i].config(image="")
        
        for i, player in enumerate(self.game.players):
            self.player_chip_labels[i].config(text=f"Chips: ${player.chips} (Bet: ${player.current_bet})")
            
            for j, card in enumerate(player.hand):
                if player.folded:
                    self.player_hand_labels[i][j].config(image="")  
                else:
                    # Show card back for AI players
                    if i > 0:  # AI players
                        self.player_hand_labels[i][j].config(image=self.card_back)
                    else:  # Human player
                        card_key = f"{card.rank.name}_of_{card.suit.name}"
                        self.player_hand_labels[i][j].config(image=self.card_images.get(card_key, self.card_back))
        
        self.pot_label.config(text=f"Pot: ${self.game.current_pot}")
        
        current_player = self.game.players[self.game.current_player_index]
        self.current_player_label.config(text=f"Current Player: {current_player.name}")
        
        for i, player in enumerate(self.game.players):
            if i == self.game.current_player_index:
                self.player_frames[i].config(bg='light yellow')
            else:
                self.player_frames[i].config(bg=self.root.cget('bg')) 
        
        is_human_turn = self.game.current_player_index == 0 
        self.fold_button.config(state=tk.NORMAL if is_human_turn else tk.DISABLED)
        self.call_button.config(state=tk.NORMAL if is_human_turn else tk.DISABLED)
        self.raise_button.config(state=tk.NORMAL if is_human_turn else tk.DISABLED)
        self.raise_entry.config(state=tk.NORMAL if is_human_turn else tk.DISABLED)
        
        if not is_human_turn:
            self.root.after(1000, self.handle_ai_turn)
    
    def show_ai_thinking(self, player_index: int, show: bool):
        if show:
            self.thinking_labels[player_index].config(text="Thinking...")
        else:
            self.thinking_labels[player_index].config(text="")
    
    def handle_fold(self):
        current_player = self.game.players[self.game.current_player_index]
        print(f"{current_player.name} folds")
        current_player.fold()
        
        active_players = [p for p in self.game.players if not p.folded]
        if len(active_players) == 1:
            winner = active_players[0]
            messagebox.showinfo("Winner", f"{winner.name} wins the pot of ${self.game.current_pot}!")
            winner.chips += self.game.current_pot
            self.update_stats(winner.name == "Human Player")
            self.reset_and_deal_new_hand()
            return
        
        self.next_player()
        
        if current_player.name == "Human Player":
            self.root.after(500, self.handle_ai_turn)
    
    def handle_call(self):
        current_player = self.game.players[self.game.current_player_index]
        
        highest_bet = max(p.current_bet for p in self.game.players)
        amount_to_call = highest_bet - current_player.current_bet
        
        amount_to_call = int(amount_to_call)
        
        if amount_to_call > 0:
            try:
                print(f"{current_player.name} calls ${amount_to_call}")
                bet_amount = current_player.bet(amount_to_call)
                self.game.current_pot += bet_amount
            except ValueError as e:
                messagebox.showerror("Error", str(e))
                return
        else:
            print(f"{current_player.name} checks")
        
        self.next_player()
        
        if current_player.name == "Human Player":
            self.root.after(500, self.handle_ai_turn)
    
    def handle_raise(self):
        raise_input = self.raise_entry.get().strip()
        
        if '.' in raise_input:
            messagebox.showerror("Invalid Raise", "Please enter a whole number (no decimals)")
            return
            
        try:
            raise_amount = int(raise_input)
            if raise_amount <= 0:
                messagebox.showerror("Invalid Raise", "Please enter a positive amount")
                return
                
            current_player = self.game.players[self.game.current_player_index]
            highest_bet = max(p.current_bet for p in self.game.players)
            amount_to_call = highest_bet - current_player.current_bet
            
            amount_to_call = int(amount_to_call)
            
            total_bet = amount_to_call + raise_amount
            
            try:
                print(f"{current_player.name} raises by ${raise_amount} (total: ${total_bet})")
                bet_amount = current_player.bet(total_bet)
                self.game.current_pot += bet_amount
                
                self.next_player()
                
                if current_player.name == "Human Player":
                    self.root.after(500, self.handle_ai_turn)
            except ValueError as e:
                messagebox.showerror("Betting Error", str(e))
        except ValueError:
            messagebox.showerror("Invalid Raise", "Please enter a valid whole number")
    
    def evaluate_round_end(self):
        active_players = [p for p in self.game.players if not p.folded]
        
        if len(active_players) == 1:
            winner = active_players[0]
            messagebox.showinfo("Winner", f"{winner.name} wins the pot of ${self.game.current_pot}!")
            winner.chips += self.game.current_pot
            self.update_stats(winner.name == "Human Player")
            self.reset_and_deal_new_hand()
            return
        
        bet_amounts = [p.current_bet for p in active_players]
        
        if len(set(bet_amounts)) == 1:
            self.advance_betting_round()
    
    def advance_betting_round(self):
        for player in self.game.players:
            player.current_bet = 0
            
        num_cards = len(self.game.community_cards)
        
        if num_cards == 0:
            print("Dealing the flop")
            self.game.deal_community_cards(3)
        elif num_cards == 3:
            print("Dealing the turn")
            self.game.deal_community_cards(1)
        elif num_cards == 4:
            print("Dealing the river")
            self.game.deal_community_cards(1)
        else:
            winner = self.game.determine_winner()
            messagebox.showinfo("Winner", f"{winner.name} wins the pot of ${self.game.current_pot}!")
            winner.chips += self.game.current_pot
            self.update_stats(winner.name == "Human Player")
            self.game.reset_game()
            self.game.deal_initial_cards()
            
        self.game.current_player_index = 0
        self.update_ui()
    
    def next_player(self):
        while True:
            self.game.current_player_index = (self.game.current_player_index + 1) % len(self.game.players)
            
            if not self.game.players[self.game.current_player_index].folded:
                break
                
            active_players = [p for p in self.game.players if not p.folded]
            if len(active_players) <= 1:
                self.evaluate_round_end()
                return
                
        self.update_ui()
    
    def handle_ai_turn(self):
        current_player = self.game.players[self.game.current_player_index]
        
        if isinstance(current_player, PokerAI):
            self.show_ai_thinking(self.game.current_player_index, True)
            self.root.update()
            
            highest_bet = max(p.current_bet for p in self.game.players)
            amount_to_call = highest_bet - current_player.current_bet
            
            amount_to_call = int(amount_to_call)
            
            action = current_player.decide_action(self.game.community_cards, amount_to_call)
            
            self.root.after(1000, lambda: self.execute_ai_action(current_player, action, amount_to_call))
    
    def execute_ai_action(self, current_player, action, amount_to_call):
        self.show_ai_thinking(self.game.current_player_index, False)
        
        if action == 'fold':
            print(f"AI {current_player.name} folds")
            current_player.fold()
            
            active_players = [p for p in self.game.players if not p.folded]
            if len(active_players) == 1:
                winner = active_players[0]
                messagebox.showinfo("Winner", f"{winner.name} wins the pot of ${self.game.current_pot}!")
                winner.chips += self.game.current_pot
                self.update_stats(winner.name == "Human Player")
                self.reset_and_deal_new_hand()
                return
        elif action == 'call':
            try:
                bet_amount = current_player.bet(amount_to_call)
                self.game.current_pot += bet_amount
                print(f"AI {current_player.name} calls ${amount_to_call}")
            except ValueError:
                current_player.fold()
                print(f"AI {current_player.name} folds (not enough chips)")
        elif action == 'raise':
            raise_amount = amount_to_call * (1 + random.random() * 2)
            raise_amount = int(raise_amount)
            if raise_amount <= 0:
                raise_amount = 1
            
            try:
                bet_amount = current_player.bet(amount_to_call + raise_amount)
                self.game.current_pot += bet_amount
                print(f"AI {current_player.name} raises by ${raise_amount}")
            except ValueError:
                try:
                    bet_amount = current_player.bet(amount_to_call)
                    self.game.current_pot += bet_amount
                    print(f"AI {current_player.name} calls ${amount_to_call} (couldn't raise)")
                except ValueError:
                    current_player.fold()
                    print(f"AI {current_player.name} folds (not enough chips)")
        
        current_idx = self.game.current_player_index
        self.next_player()
        
        next_player_is_human = self.game.current_player_index == 0
        if next_player_is_human:
            self.evaluate_round_end()
        else:
            self.root.after(1000, self.handle_ai_turn)
    
    def reset_and_deal_new_hand(self):
        self.game.reset_game()
        self.game.deal_initial_cards()
        
        small_blind_pos = 1 % len(self.game.players)
        big_blind_pos = 2 % len(self.game.players)
        
        small_blind = int(self.game.small_blind)
        self.game.players[small_blind_pos].bet(small_blind)
        self.game.current_pot += small_blind
        print(f"{self.game.players[small_blind_pos].name} posts small blind: ${small_blind}")
        
        big_blind = int(self.game.small_blind * 2)
        self.game.players[big_blind_pos].bet(big_blind)
        self.game.current_pot += big_blind
        print(f"{self.game.players[big_blind_pos].name} posts big blind: ${big_blind}")
        
        self.game.current_player_index = 0
        self.update_ui()
    
    def start_game(self):
        self.game.deck.shuffle()
        self.game.deal_initial_cards()
        
        self.game.current_player_index = 0
        
        small_blind_pos = 1 % len(self.game.players)
        big_blind_pos = 2 % len(self.game.players)
        
        small_blind = int(self.game.small_blind)
        self.game.players[small_blind_pos].bet(small_blind)
        self.game.current_pot += small_blind
        print(f"{self.game.players[small_blind_pos].name} posts small blind: ${small_blind}")
        
        big_blind = int(self.game.small_blind * 2)
        self.game.players[big_blind_pos].bet(big_blind)
        self.game.current_pot += big_blind
        print(f"{self.game.players[big_blind_pos].name} posts big blind: ${big_blind}")
        
        self.update_ui()
        
        self.root.mainloop()

# Test Example
if __name__ == "__main__":
    from src.game.Game import PokerGame  
    
    game = PokerGame(["Player 1", "AI Player 1", "AI Player 2"])
    
    ui = PokerGameUI(game, card_image_path='path/to/your/card/images/')
    ui.start_game()