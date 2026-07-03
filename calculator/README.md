# TaskFlow Calculator - Multi-Mode CLI & GUI

A highly polished, multi-mode **Calculator** application implemented in Python. TaskFlow Calculator features both a terminal command-line prompt mode (CLI) and a stunning desktop graphical user interface (GUI) with unified entry controls.

---

## Features

### 💻 Graphical User Interface (GUI) Mode
- **Premium Dark Mode**: Built with deep charcoal backgrounds, responsive button highlights, and clean typography.
- **Dynamic Equations**: Displays the expression as it builds, along with real-time result outputs.
- **Sliding History Panel**: A slide-out panel that expands the window to show scrolling logs of previous calculations. Double-clicking any history item loads it directly back into the entry display.
- **Keyboard Hook Bindings**: Input numbers and symbols (`0-9`, `+`, `-`, `*`, `/`, `%`, `^`, `.`, `Enter` for calculation, `Backspace` for delete, `Escape` for clear) directly from your keyboard.
- **Validation**: Smart checks prevent invalid consecutive operators or multiple decimal points in a single value.

### 📟 Command-Line Interface (CLI) Mode
- **Interactive Prompts**: Sequential prompts ask for Number 1, Number 2, and the math operator.
- **Float Conversion Checks**: Validates numeric input and handles edge cases securely.
- **ASCII Box Layouts**: Outputs results inside styled text dividers for high console readability.

---

## File Structure

```text
calculator/
├── .gitignore          # Excludes temporary cache files
├── README.md           # This task documentation
├── main.py             # App router and entry controller
├── cli_calc.py         # Terminal CLI interactive logic
└── gui_calc.py         # Desktop Tkinter GUI logic
```

---

## How to Run

Navigate to the project root directory and execute:

### 1. Run GUI Desktop Mode (Default)
```bash
python "calculator/main.py"
```

### 2. Run CLI Command-Line Mode
```bash
python "calculator/main.py" --cli
```

---

## Mathematical Capabilities
- `+` Addition
- `-` Subtraction
- `*` Multiplication
- `/` Division (with divide-by-zero checks)
- `%` Modulo (remainder division)
- `^` Exponentiation (power raising with overflow protection)
