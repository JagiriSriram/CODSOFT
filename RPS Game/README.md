# Rock-Paper-Scissors Game - Multi-Mode CLI & GUI

A highly polished, multi-mode **Rock-Paper-Scissors** game built with Python. Features an interactive command-line interface (CLI) for classic terminal play and a premium desktop graphical user interface (GUI) with scoreboards and custom weapon card buttons.

---

## Features

### 💻 Graphical User Interface (GUI) Mode
- **Mocha Dark Styling**: Features custom card grids, dark slate backgrounds, and custom button highlights.
- **Persistent Scoreboard**: A header bar records Player Wins, Computer Wins, and Tie rounds.
- **Dynamic Battle Arena**: Displays selection cards side by side (✊ Rock, ✋ Paper, ✌️ Scissors) showing the chosen weapons for Player vs Computer.
- **Outcome Status Banner**: A wide banner dynamically changes colors (Green for Win, Red for Loss, Orange for Tie) to provide immediate outcome feedback.
- **Reset Scores**: Dedicated control button clears scoreboard records.

### 📟 Command-Line Interface (CLI) Mode
- **Weapon Selector Menu**: Classic menu selectors: 1 (Rock), 2 (Paper), 3 (Scissors), or Q (Quit).
- **Framed Outcome Results**: Prints clean ASCII horizontal border summaries of choices and round results.
- **Score Logging**: Logs totals at the end of each round and prompts "Do you want to play again?".

---

## File Structure

```text
RPS Game/
├── .gitignore      # Excludes temporary cache folders
├── README.md       # This game instructions guide
├── main.py         # App router and launcher entry point
├── cli_game.py     # Terminal prompt game loop
└── gui_game.py     # Desktop Tkinter GUI with battle cards
```

---

## How to Run

Navigate to the project root directory and execute:

### 1. Launch GUI Desktop Mode (Default)
```bash
python "RPS Game/main.py"
```

### 2. Launch CLI Command-Line Mode
```bash
python "RPS Game/main.py" --cli
```

---

## Game Rules
- **Rock (✊) beats Scissors (✌️)**
- **Scissors (✌️) beat Paper (✋)**
- **Paper (✋) beats Rock (✊)**
- Emojis are displayed for all choices. If a round features identical selections, it is declared a Tie.
