# Contact Book - Multi-Mode CLI & GUI

A highly polished, multi-mode **Contact Book** manager application built with Python. TaskFlow Contact Book persists records locally using an SQLite database, offering both an interactive console prompt interface (CLI) and a premium, responsive desktop graphical user interface (GUI).

---

## Features

### 💻 Graphical User Interface (GUI) Mode
- **Mocha Dark Styling**: Features custom card layouts, sidebar index lists, and responsive text inputs.
- **Left Sidebar**: A scrollable Listbox displaying contact names and phone numbers, with a real-time search input bar at the top (filters contacts dynamically as you type).
- **Details Card Pane**: Displays the selected contact's complete information: Name, Phone, Email, and Address.
- **Initials Avatar Canvas**: Dynamically draws a custom circular profile icon using the initials of the selected contact's name.
- **Modal Modifying Dialogs**: Custom pop-up forms prompt users to Add or Edit contact fields, with validation checks ensuring Name and Phone are entered.
- **Interactive Deletions**: Deleting a contact prompts a confirmation popup and clears the UI panel.

### 📟 Command-Line Interface (CLI) Mode
- **Structured Operation List**: Menu selectors: 1 (List All), 2 (Add), 3 (Search), 4 (Update), 5 (Delete), or Q (Quit).
- **Formatted Tabular Lists**: Displays ID, Name, and Phone in aligned horizontal terminal grids.
- **Interactive Forms**: Prompts for inputs showing current values inside parentheses during updates.

---

## File Structure

```text
contact book/
├── .gitignore          # Excludes local databases and python caches
├── README.md           # This project guide
├── main.py             # App router and launcher entry point
├── db_contacts.py      # Shared SQLite database manager CRUD
├── cli_contacts.py     # Terminal prompt flow
└── gui_contacts.py     # Desktop Tkinter GUI with avatars and detail cards
```

---

## How to Run

Navigate to the project root directory and execute:

### 1. Launch GUI Desktop Mode (Default)
```bash
python "contact book/main.py"
```

### 2. Launch CLI Command-Line Mode
```bash
python "contact book/main.py" --cli
```

---

## Database Schema
Data is persisted in the local SQLite database file `contacts.db` with the following columns:
- `id` (INTEGER PRIMARY KEY)
- `name` (TEXT NOT NULL)
- `phone` (TEXT NOT NULL)
- `email` (TEXT)
- `address` (TEXT)
- `created_at` (TEXT)
