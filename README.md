# TaskFlow - Premium Python GUI To-Do List

A modern, fast, and feature-rich **To-Do List** application built with Python. TaskFlow features an elegant dark mode user interface, local data persistence using SQLite, dynamic search, multi-criteria filtering, and priority visual coding.

---

## Key Features

- ⚡ **Local Persistence**: Powered by Python's built-in `sqlite3` database. Your tasks are saved automatically and remain intact when you close the app.
- 🎨 **Rich Modern Aesthetics**: Sleek dark mode styling featuring Catppuccin Mocha colors, rounded card hovers, and clean typography.
- 🏷️ **Categorized Organization**: Group tasks into custom or standard categories (e.g., Work, Personal, Shopping, Health) and view real-time counts.
- ⚖️ **Priority Levels**: Tasks are color-coded (Red for High, Orange for Medium, Green for Low) with left border accents.
- 📅 **Due Dates**: Track deadlines. Tasks display standard dates, and past deadlines are colored red with an "Overdue" indicator.
- 🔍 **Real-time Search & Filter**: Search by title or description in real-time as you type, filter by status (All, Pending, Completed), and filter by category chips.
- 🔃 **Sorting Controls**: Sort tasks dynamically by creation time (Newest First), due date, or priority.

---

## File Structure

```text
codSoft/
├── .gitignore
├── README.md
└── To-Do list/
    ├── main.py             # Main entry point and core controller
    ├── db_manager.py       # SQLite database operations & filters
    └── gui_components.py   # Reusable GUI frames, cards, and modal forms
```

---

## Requirements

TaskFlow uses Python's standard library modules and has **no external dependencies**. You do not need to install any external pip packages.
- Python 3.8 or higher is recommended.
- Tkinter (standard with Python on Windows/macOS).

---

## How to Run the Application

Navigate to the project root directory and execute:

```bash
python "To-Do list/main.py"
```

---

## Core Technologies

- **Language**: Python 3
- **GUI Engine**: Tkinter / ttk
- **Database Engine**: SQLite 3
