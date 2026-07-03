import tkinter as tk
from tkinter import ttk, messagebox
import random

# Theme Palette (Consistent with other portfolio apps)
THEME = {
    "bg_main": "#1e1e2e",       # Deep mocha background
    "bg_card": "#252538",       # Selection cards
    "bg_header": "#181825",     # Scoreboard panel
    "fg_text": "#cdd6f4",       # Primary light text
    "fg_sub": "#7f849c",        # Muted text
    "accent": "#89b4fa",        # Blue accent
    "accent_hover": "#b4befe",  # Hover blue
    "white": "#ffffff",
    "black": "#11111b",
    
    # Outcomes colors
    "win": "#a6e3a1",           # Green
    "lose": "#f38ba8",          # Red
    "tie": "#fab387"            # Orange
}

class HoverButton(tk.Button):
    """Custom flat buttons with color-coded hover highlights."""
    def __init__(self, parent, hover_bg, normal_bg, *args, **kwargs):
        super().__init__(parent, bg=normal_bg, activebackground=hover_bg, bd=0, relief="flat", **kwargs)
        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.bind("<Enter>", lambda e: self.config(bg=self.hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self.normal_bg))


class GUIGame(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, bg=THEME["bg_main"], **kwargs)
        self.parent = parent
        self.parent.title("Rock-Paper-Scissors")
        self.parent.geometry("500x580")
        self.parent.resizable(False, False)
        self.parent.configure(bg=THEME["bg_main"])

        # Scores State
        self.player_score = 0
        self.computer_score = 0
        self.ties_score = 0

        self.weapons = {
            'rock': {'emoji': '✊', 'name': 'Rock'},
            'paper': {'emoji': '✋', 'name': 'Paper'},
            'scissors': {'emoji': '✌️', 'name': 'Scissors'}
        }

        self.center_window()
        self._build_ui()

    def center_window(self):
        self.parent.update_idletasks()
        width = 500
        height = 580
        x = (self.parent.winfo_screenwidth() // 2) - (width // 2)
        y = (self.parent.winfo_screenheight() // 2) - (height // 2)
        self.parent.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self):
        # Scoreboard Header Panel
        self.score_frame = tk.Frame(self, bg=THEME["bg_header"], height=70)
        self.score_frame.pack(fill="x", side="top")
        self.score_frame.pack_propagate(False)

        # Labels for scoreboard
        score_font = ("Segoe UI", 11, "bold")
        self.player_score_lbl = tk.Label(
            self.score_frame, 
            text="PLAYER: 0", 
            font=score_font, 
            fg=THEME["accent"], 
            bg=THEME["bg_header"]
        )
        self.player_score_lbl.pack(side="left", expand=True)

        self.ties_score_lbl = tk.Label(
            self.score_frame, 
            text="TIES: 0", 
            font=score_font, 
            fg=THEME["fg_sub"], 
            bg=THEME["bg_header"]
        )
        self.ties_score_lbl.pack(side="left", expand=True)

        self.computer_score_lbl = tk.Label(
            self.score_frame, 
            text="COMPUTER: 0", 
            font=score_font, 
            fg=THEME["lose"], 
            bg=THEME["bg_header"]
        )
        self.computer_score_lbl.pack(side="left", expand=True)

        # Battle Arena Panel (Selection Cards side by side)
        self.arena_frame = tk.Frame(self, bg=THEME["bg_main"], pady=20)
        self.arena_frame.pack(fill="both")

        # Player Choice Card
        self.p_card = tk.Frame(self.arena_frame, bg=THEME["bg_card"], width=160, height=180)
        self.p_card.pack(side="left", expand=True, padx=(40, 10))
        self.p_card.pack_propagate(False)

        tk.Label(self.p_card, text="Player Weapon", font=("Segoe UI", 10), fg=THEME["fg_sub"], bg=THEME["bg_card"], pady=10).pack()
        self.p_emoji_lbl = tk.Label(self.p_card, text="❓", font=("Segoe UI", 48), fg=THEME["white"], bg=THEME["bg_card"])
        self.p_emoji_lbl.pack(expand=True)
        self.p_name_lbl = tk.Label(self.p_card, text="Pending...", font=("Segoe UI", 11, "bold"), fg=THEME["fg_text"], bg=THEME["bg_card"], pady=10)
        self.p_name_lbl.pack()

        # Versus Label
        vs_lbl = tk.Label(self.arena_frame, text="VS", font=("Segoe UI", 20, "bold italic"), fg=THEME["fg_sub"], bg=THEME["bg_main"])
        vs_lbl.pack(side="left", expand=True)

        # Computer Choice Card
        self.c_card = tk.Frame(self.arena_frame, bg=THEME["bg_card"], width=160, height=180)
        self.c_card.pack(side="right", expand=True, padx=(10, 40))
        self.c_card.pack_propagate(False)

        tk.Label(self.c_card, text="Computer Weapon", font=("Segoe UI", 10), fg=THEME["fg_sub"], bg=THEME["bg_card"], pady=10).pack()
        self.c_emoji_lbl = tk.Label(self.c_card, text="❓", font=("Segoe UI", 48), fg=THEME["white"], bg=THEME["bg_card"])
        self.c_emoji_lbl.pack(expand=True)
        self.c_name_lbl = tk.Label(self.c_card, text="Pending...", font=("Segoe UI", 11, "bold"), fg=THEME["fg_text"], bg=THEME["bg_card"], pady=10)
        self.c_name_lbl.pack()

        # Outcome Banner Bar
        self.outcome_frame = tk.Frame(self, bg="#313244", height=50)
        self.outcome_frame.pack(fill="x", pady=15)
        self.outcome_frame.pack_propagate(False)

        self.outcome_lbl = tk.Label(
            self.outcome_frame,
            text="Choose your weapon below to start!",
            font=("Segoe UI", 12, "bold"),
            fg=THEME["fg_text"],
            bg="#313244"
        )
        self.outcome_lbl.pack(fill="both", expand=True)

        # Weapons Selection Panel
        weapons_frame = tk.Frame(self, bg=THEME["bg_main"], padx=20)
        weapons_frame.pack(fill="x")
        
        tk.Label(
            weapons_frame,
            text="CHOOSE YOUR WEAPON",
            font=("Segoe UI", 8, "bold"),
            fg=THEME["fg_sub"],
            bg=THEME["bg_main"]
        ).pack(anchor="center", pady=(0, 10))

        btn_container = tk.Frame(weapons_frame, bg=THEME["bg_main"])
        btn_container.pack(fill="x")

        # Create styled weapon cards as buttons
        for code, details in self.weapons.items():
            self._create_weapon_button(btn_container, code, details)

        # Footer Actions Panel
        footer_frame = tk.Frame(self, bg=THEME["bg_main"], pady=15)
        footer_frame.pack(fill="both", side="bottom")

        # Reset Scores Button
        self.reset_btn = HoverButton(
            footer_frame,
            hover_bg=THEME["win"],
            normal_bg=THEME["bg_card"],
            text="🔄 Reset Scores",
            font=("Segoe UI", 9, "bold"),
            fg=THEME["fg_text"],
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.reset_game
        )
        self.reset_btn.pack(anchor="center")

    def _create_weapon_button(self, parent, code, details):
        """Creates custom weapon buttons with large emojis."""
        btn_bg = THEME["bg_card"]
        btn_hover = THEME["bg_main"] # Note: Hover highlights

        frame = tk.Frame(parent, bg=THEME["bg_card"], bd=0, highlightthickness=1, highlightbackground="#313244")
        frame.pack(side="left", expand=True, padx=5, fill="both")

        btn = HoverButton(
            frame,
            hover_bg="#313244",
            normal_bg=THEME["bg_card"],
            text=f"{details['emoji']}\n{details['name']}",
            font=("Segoe UI", 12, "bold"),
            fg=THEME["white"],
            height=3,
            pady=10,
            cursor="hand2",
            command=lambda: self.play_round(code)
        )
        btn.pack(fill="both", expand=True)

    def play_round(self, player_choice):
        """Determine winner, animate outcome banner, and increment scoreboard."""
        computer_choice = random.choice(list(self.weapons.keys()))

        # Update visuals in battle arena
        p_weapon = self.weapons[player_choice]
        c_weapon = self.weapons[computer_choice]

        self.p_emoji_lbl.config(text=p_weapon['emoji'])
        self.p_name_lbl.config(text=p_weapon['name'].upper())

        self.c_emoji_lbl.config(text=c_weapon['emoji'])
        self.c_name_lbl.config(text=c_weapon['name'].upper())

        # Determine round results
        result = self._evaluate_winner(player_choice, computer_choice)

        if result == 'win':
            self.player_score += 1
            self.player_score_lbl.config(text=f"PLAYER: {self.player_score}")
            
            # Configure Win Banner
            self.outcome_lbl.config(text=f"🎉 YOU WIN! {p_weapon['name']} beats {c_weapon['name']}.", fg=THEME["black"])
            self.outcome_frame.config(bg=THEME["win"])
            self.outcome_lbl.config(bg=THEME["win"])
        elif result == 'lose':
            self.computer_score += 1
            self.computer_score_lbl.config(text=f"COMPUTER: {self.computer_score}")

            # Configure Loss Banner
            self.outcome_lbl.config(text=f"😢 YOU LOSE! {c_weapon['name']} beats {p_weapon['name']}.", fg=THEME["black"])
            self.outcome_frame.config(bg=THEME["lose"])
            self.outcome_lbl.config(bg=THEME["lose"])
        else:
            self.ties_score += 1
            self.ties_score_lbl.config(text=f"TIES: {self.ties_score}")

            # Configure Tie Banner
            self.outcome_lbl.config(text=f"🤝 IT'S A TIE! Both selected {p_weapon['name']}.", fg=THEME["black"])
            self.outcome_frame.config(bg=THEME["tie"])
            self.outcome_lbl.config(bg=THEME["tie"])

    def _evaluate_winner(self, player, computer):
        if player == computer:
            return 'tie'
        if (player == 'rock' and computer == 'scissors') or \
           (player == 'scissors' and computer == 'paper') or \
           (player == 'paper' and computer == 'rock'):
            return 'win'
        return 'lose'

    def reset_game(self):
        """Resets scoreboard and arena display states."""
        confirm = messagebox.askyesno("Reset Game", "Are you sure you want to reset all scores?")
        if confirm:
            self.player_score = 0
            self.computer_score = 0
            self.ties_score = 0

            self.player_score_lbl.config(text="PLAYER: 0")
            self.computer_score_lbl.config(text="COMPUTER: 0")
            self.ties_score_lbl.config(text="TIES: 0")

            # Reset Displays
            self.p_emoji_lbl.config(text="❓")
            self.p_name_lbl.config(text="Pending...")
            self.c_emoji_lbl.config(text="❓")
            self.c_name_lbl.config(text="Pending...")

            # Reset Banner
            self.outcome_lbl.config(text="Choose your weapon below to start!", fg=THEME["fg_text"])
            self.outcome_frame.config(bg="#313244")
            self.outcome_lbl.config(bg="#313244")

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIGame(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
