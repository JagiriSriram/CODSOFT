# Password Generator - Multi-Mode CLI & GUI

A modern, highly secure **Password Generator** application built with Python. TaskFlow Password Generator creates cryptographically secure random passwords using Python's `secrets` module, supporting both an interactive console prompt interface (CLI) and a premium desktop graphical user interface (GUI).

---

## Features

### 💻 Graphical User Interface (GUI) Mode
- **Mocha Dark Styling**: Features custom layouts with clean borders, slider scales, and rounded button highlights.
- **Dynamic Adjustments**: Slider modifies password length (from 4 to 64 characters) and automatically regenerates the password instantly.
- **Complexity Selectors**: Toggle Uppercase, Lowercase, Numbers, and Symbols. Changing any parameter refreshes the password instantly.
- **Visual Strength Analyzer**: A segmented progress bar evaluates password strength (Weak, Medium, Strong, Very Strong) in matching security colors (Red, Orange, Yellow, Green).
- **One-Click Copy**: A dedicated button saves the password to your clipboard and slides out a green confirmation bar.

### 📟 Command-Line Interface (CLI) Mode
- **Interactive Menu Flow**: Asks for length and prompts y/n questions for character complexity.
- **Numeric Validation**: Verifies length integer ranges.
- **Secure Shuffling**: Guarantees that at least one character from each selected subset is included in the output.

---

## File Structure

```text
password generator/
├── .gitignore          # Excludes compiled files
├── README.md           # This task guide
├── main.py             # App router and entry point
├── cli_generator.py    # Console prompt flow
└── gui_generator.py    # Desktop Tkinter GUI with strength metrics
```

---

## How to Run

Navigate to the project root directory and execute:

### 1. Run GUI Desktop Mode (Default)
```bash
python "password generator/main.py"
```

### 2. Run CLI Command-Line Mode
```bash
python "password generator/main.py" --cli
```

---

## Cryptographic Security
This application utilizes Python's built-in **`secrets`** module to generate character indexes. Unlike `random`, `secrets` uses the operating system's highest-quality secure random number generator (CSPRNG), making it safe for passwords and security keys.
