# Texas Hold'em Poker AI Project

## System Requirements

### Operating System
- macOS 10.15 or higher
- Windows 10 or higher
- Linux (Ubuntu 20.04 or higher)

### Requirements
- Python 3.8 or higher
- tkinter (usually included with Python, but may need to be installed separately on Linux)
- treys==0.1.8
- Pillow==10.2.0


## Installation Instructions

1. **Clone the repository or download as zip file**
```bash
# To clone the repository these are the command lines
git clone https://github.com/LiamB2222/4_of_a_kind.git
cd 4_of_a_kind
```

2. **Create and activate a virtual environment**
```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

## Running the Application

1. **Start the game**
```bash
python main.py or python3 main.py (depending on you machine)
```

2. **Directory Structure**
Make sure the `CARD` folder containing card images is in the root directory:
```
4_of_a_kind/
├── main.py
├── Game.py
├── Player.py
├── AI_Player.py
├── UI.py
├── pWin.py
├── Deck.py
└── CARD/
    └── [card images]
```

## Troubleshooting

### 1. **Card images not showing up**

If the card images are missing or not displaying correctly:

- Ensure that the `CARD/` folder with the card images is **located in the root directory** of the project.
- If the `CARD/` folder is missing or misplaced, the game will use placeholder images instead of actual cards.
  
### 2. **`tkinter` not found (GUI not working)**

If you see an error related to `tkinter`, it might be missing on your system (mostly for Linux or certain Python installations):

- **macOS/Windows**: `tkinter` is usually bundled with Python. Make sure you’re using the Python version from [python.org](https://www.python.org/downloads/).
  
- **Linux (Ubuntu/Debian)**:
  You may need to install the `tkinter` package manually:
  ```bash
  sudo apt-get install python3-tk

### 3. Libraries not intalled
If you are stil having issues even after using the requirements.txt install each library manually on your terminal.
- **Treys**
```bash
pip install treys
```
- **Pillow**
```bash
pip install Pillow
```

## How to Play

1. The game starts with you and one AI opponent
2. Each player starts with 1000 chips
3. Standard Texas Hold'em rules apply:
   - Small blind: 10 chips
   - Big blind: 20 chips
   - Four betting rounds: Pre-flop, Flop, Turn, River

## Controls
- Use the GUI buttons to:
  - Check/Call
  - Raise
  - Fold

## Test Configuration
- Default player name: "You"
- Default AI opponent: "AI Player 1"
- Starting chips: 1000 for all players

## Troubleshooting

If card images don't appear:
1. Verify the `CARD` folder is in the correct location
2. Check Python's Pillow installation
3. The game will use placeholder images if cards aren't found

## Development Notes

- Monte Carlo simulation is used for AI decision making
- The `treys` library handles hand evaluation
- GUI built with tkinter for cross-platform compatibility

## Texas Hold'em Poker Rules
### 1. The Objective
- Make the best 5-card poker hand using your two hole cards and five community cards on the table.
### 2. The Setup
- Each player gets 2 private cards (hole cards).
- Then 5 community cards are dealt face-up in the center:
    - 3 cards (the flop)
    - 1 card (the turn)
    - 1 card (the river)
### 3. The Rounds of Betting
- There are four betting rounds:
    - Pre-Flop: after players get their hole cards.
    - Flop: after the first 3 community cards are revealed.
    - Turn: after the 4th community card is revealed.
    - River: after the 5th and final community card is revealed.
### 4. Betting Options
- Fold: Quit the current hand and give up your chance to win the pot.
- Check/Call (same button): Do nothing if no one has bet or Match another player's bet.
- Bet: Put chips into the pot.
- Raise: Increase the bet amount.
### 5. The Best Hand Wins
- After the final betting round, if more than one player remains, a showdown happens:
    - Players reveal their cards.
    - The best 5-card hand wins the pot.
### 6. Hand Rankings (High to Low)
1. Royal Flush
2. Straight Flush
3. Four of a Kind
4. Full House
5. Flush
6. Straight
7. Three of a Kind
8. Two Pair
9. One Pair
10. High Card
