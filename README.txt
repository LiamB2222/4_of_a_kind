# Texas Hold'em Poker AI Project

## System Requirements

### Operating System
- macOS 10.15 or higher
- Windows 10 or higher
- Linux (Ubuntu 20.04 or higher)

### Language/Runtime
- Python 3.8 or higher

### Required Libraries
- treys==0.1.8 (Poker hand evaluation)
- Pillow==10.2.0 (Image processing)
- tkinter>=8.6 (GUI framework, included with Python)

## Installation Instructions

1. **Clone the repository**
```bash
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
python main.py
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
- Slider control for adjusting raise amounts

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