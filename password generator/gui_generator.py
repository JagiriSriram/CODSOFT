import tkinter as tk
from tkinter import ttk, messagebox
import string
import secrets

# Theme Palette
THEME = {
    "bg_main": "#1e1e2e",       # Deep mocha background
    "bg_card": "#252538",       # Section panels
    "bg_display": "#181825",    # Password read-only display
    "fg_text": "#cdd6f4",       # Primary light text
    "fg_sub": "#7f849c",        # Secondary muted text
    "accent": "#89b4fa",        # Accent blue
    "accent_hover": "#b4befe",  # Hover blue
    "white": "#ffffff",
    "black": "#11111b",
    
    # Strength Colors
    "weak": "#f38ba8",          # Red
    "medium": "#fab387",        # Orange
    "strong": "#f9e2af",        # Yellow
    "vstrong": "#a6e3a1"        # Green
}

class HoverButton(tk.Button):
    """Custom button with hover active styling."""
    def __init__(self, parent, hover_bg, normal_bg, *args, **kwargs):
        super().__init__(parent, bg=normal_bg, activebackground=hover_bg, bd=0, relief="flat", **kwargs)
        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.bind("<Enter>", lambda e: self.config(bg=self.hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self.normal_bg))


class StrengthMeter(tk.Canvas):
    """A custom drawing canvas representing password security levels in colored segments."""
    def __init__(self, parent, width=150, height=14, **kwargs):
        super().__init__(parent, width=width, height=height, bg=THEME["bg_display"], 
                         highlightthickness=0, **kwargs)
        self.width = width
        self.height = height
        self.set_strength(1)  # Default: Weak

    def set_strength(self, level):
        """
        level: 1 (Weak), 2 (Medium), 3 (Strong), 4 (Very Strong)
        """
        self.delete("all")
        
        # Colors depending on strength
        colors = {
            1: (THEME["weak"], "Weak"),
            2: (THEME["medium"], "Medium"),
            3: (THEME["strong"], "Strong"),
            4: (THEME["vstrong"], "Very Strong")
        }
        color, text = colors.get(level, (THEME["weak"], "Weak"))

        # Draw 4 segmented blocks
        num_blocks = 4
        block_width = (self.width - (num_blocks - 1) * 4) // num_blocks
        
        for i in range(num_blocks):
            x0 = i * (block_width + 4)
            x1 = x0 + block_width
            
            # Active vs inactive segment filling
            fill_color = color if i < level else "#313244"
            
            self.create_rectangle(
                x0, 0, x1, self.height, 
                fill=fill_color, outline="", width=0
            )


class GUIPasswordGenerator(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, bg=THEME["bg_main"], **kwargs)
        self.parent = parent
        self.parent.title("TaskFlow - Secure Password Generator")
        self.parent.geometry("460x520")
        self.parent.resizable(False, False)
        self.parent.configure(bg=THEME["bg_main"])

        # Center Window
        self.center_window()

        self._build_ui()
        self.generate()  # Run initial generation

    def center_window(self):
        self.parent.update_idletasks()
        width = 460
        height = 520
        x = (self.parent.winfo_screenwidth() // 2) - (width // 2)
        y = (self.parent.winfo_screenheight() // 2) - (height // 2)
        self.parent.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self):
        container = tk.Frame(self, bg=THEME["bg_main"], padx=20, pady=20)
        container.pack(fill="both", expand=True)

        # Header Frame
        header = tk.Frame(container, bg=THEME["bg_main"])
        header.pack(fill="x", pady=(0, 20))
        
        logo_lbl = tk.Label(
            header,
            text="🔑 Password Generator",
            font=("Segoe UI", 18, "bold"),
            fg=THEME["accent"],
            bg=THEME["bg_main"]
        )
        logo_lbl.pack(anchor="w")
        
        subtitle_lbl = tk.Label(
            header,
            text="Generate strong, cryptographically secure passwords instantly.",
            font=("Segoe UI", 9),
            fg=THEME["fg_sub"],
            bg=THEME["bg_main"]
        )
        subtitle_lbl.pack(anchor="w", pady=(2, 0))

        # Output Display Panel
        display_panel = tk.Frame(container, bg=THEME["bg_display"], padx=15, pady=15, bd=0)
        display_panel.pack(fill="x", pady=(0, 20))

        # Row 1: Password String Box & Copy Button
        row1 = tk.Frame(display_panel, bg=THEME["bg_display"])
        row1.pack(fill="x")

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            row1,
            textvariable=self.password_var,
            font=("Consolas", 14, "bold"),
            fg=THEME["white"],
            bg=THEME["bg_display"],
            bd=0,
            insertbackground="white",
            state="readonly",
            readonlybackground=THEME["bg_display"]
        )
        self.password_entry.pack(side="left", fill="x", expand=True)

        # Copy Button
        copy_btn = HoverButton(
            row1,
            hover_bg=THEME["accent_hover"],
            normal_bg=THEME["accent"],
            text="📋 Copy",
            font=("Segoe UI", 9, "bold"),
            fg=THEME["black"],
            cursor="hand2",
            padx=12,
            pady=6,
            command=self.copy_to_clipboard
        )
        copy_btn.pack(side="right", padx=(10, 0))

        # Row 2: Divider
        divider = tk.Frame(display_panel, bg="#313244", height=1)
        divider.pack(fill="x", pady=10)

        # Row 3: Strength Meter display
        row3 = tk.Frame(display_panel, bg=THEME["bg_display"])
        row3.pack(fill="x")

        tk.Label(
            row3,
            text="Security Strength:",
            font=("Segoe UI", 9, "bold"),
            fg=THEME["fg_sub"],
            bg=THEME["bg_display"]
        ).pack(side="left")

        # Custom Segmented Strength Meter
        self.strength_meter = StrengthMeter(row3, width=140, height=12)
        self.strength_meter.pack(side="left", padx=10)

        self.strength_lbl = tk.Label(
            row3,
            text="Weak",
            font=("Segoe UI", 9, "bold"),
            fg=THEME["weak"],
            bg=THEME["bg_display"]
        )
        self.strength_lbl.pack(side="left")

        # Configuration Panel (Card Frame)
        config_card = tk.Frame(container, bg=THEME["bg_card"], padx=20, pady=20)
        config_card.pack(fill="both", expand=True)

        # Slider for length
        slider_row = tk.Frame(config_card, bg=THEME["bg_card"])
        slider_row.pack(fill="x", pady=(0, 15))

        self.len_lbl = tk.Label(
            slider_row,
            text="Password Length: 12",
            font=("Segoe UI", 10, "bold"),
            fg=THEME["white"],
            bg=THEME["bg_card"]
        )
        self.len_lbl.pack(side="left")

        # Track slider changes in real-time
        self.length_var = tk.IntVar(value=12)
        self.slider = ttk.Scale(
            config_card,
            from_=4,
            to=64,
            variable=self.length_var,
            orient="horizontal",
            command=self._on_slider_move
        )
        self.slider.pack(fill="x", pady=(0, 20))

        # Complexity checkbox filters
        tk.Label(
            config_card,
            text="COMPLEXITY PARAMETERS",
            font=("Segoe UI", 8, "bold"),
            fg=THEME["fg_sub"],
            bg=THEME["bg_card"]
        ).pack(anchor="w", pady=(0, 10))

        # Grid of checkboxes
        checkbox_frame = tk.Frame(config_card, bg=THEME["bg_card"])
        checkbox_frame.pack(fill="x")
        checkbox_frame.columnconfigure(0, weight=1)
        checkbox_frame.columnconfigure(1, weight=1)

        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=False)

        # Styled Checkbutton definitions
        chk1 = tk.Checkbutton(checkbox_frame, text="Uppercase (A-Z)", variable=self.use_upper, font=("Segoe UI", 10), bg=THEME["bg_card"], fg=THEME["fg_text"], selectcolor=THEME["bg_main"], activebackground=THEME["bg_card"], activeforeground=THEME["white"], command=self.generate)
        chk1.grid(row=0, column=0, sticky="w", pady=5)

        chk2 = tk.Checkbutton(checkbox_frame, text="Lowercase (a-z)", variable=self.use_lower, font=("Segoe UI", 10), bg=THEME["bg_card"], fg=THEME["fg_text"], selectcolor=THEME["bg_main"], activebackground=THEME["bg_card"], activeforeground=THEME["white"], command=self.generate)
        chk2.grid(row=0, column=1, sticky="w", pady=5)

        chk3 = tk.Checkbutton(checkbox_frame, text="Numbers (0-9)", variable=self.use_digits, font=("Segoe UI", 10), bg=THEME["bg_card"], fg=THEME["fg_text"], selectcolor=THEME["bg_main"], activebackground=THEME["bg_card"], activeforeground=THEME["white"], command=self.generate)
        chk3.grid(row=1, column=0, sticky="w", pady=5)

        chk4 = tk.Checkbutton(checkbox_frame, text="Symbols (!@#$)", variable=self.use_symbols, font=("Segoe UI", 10), bg=THEME["bg_card"], fg=THEME["fg_text"], selectcolor=THEME["bg_main"], activebackground=THEME["bg_card"], activeforeground=THEME["white"], command=self.generate)
        chk4.grid(row=1, column=1, sticky="w", pady=5)

        # Action Buttons row
        btn_row = tk.Frame(container, bg=THEME["bg_main"])
        btn_row.pack(fill="x", side="bottom", pady=(15, 0))

        # Generate Button
        self.gen_btn = HoverButton(
            btn_row,
            hover_bg=THEME["accent_hover"],
            normal_bg=THEME["accent"],
            text="🔄 Generate Password",
            font=("Segoe UI", 11, "bold"),
            fg=THEME["black"],
            cursor="hand2",
            pady=10,
            command=self.generate
        )
        self.gen_btn.pack(fill="x")

        # Placeholder label for temporary copy notifications
        self.notify_lbl = None

    def _on_slider_move(self, value):
        length = int(float(value))
        self.len_lbl.config(text=f"Password Length: {length}")
        # Automatically generate on slide movement
        self.generate()

    def generate(self):
        """Fetch settings, calculate random password, and analyze security strength."""
        length = self.length_var.get()
        upper = self.use_upper.get()
        lower = self.use_lower.get()
        digits = self.use_digits.get()
        symbols = self.use_symbols.get()

        # Handle empty parameter inputs
        if not (upper or lower or digits or symbols):
            self.password_var.set("Select parameters...")
            self.strength_meter.set_strength(0)
            self.strength_lbl.config(text="None", fg=THEME["fg_sub"])
            return

        # Generate
        password = self.generate_secure_password_logic(length, upper, lower, digits, symbols)
        self.password_var.set(password)
        
        # Analyze Strength
        self.evaluate_strength(password, upper, lower, digits, symbols)

    def generate_secure_password_logic(self, length, use_upper, use_lower, use_digits, use_symbols):
        upper_chars = string.ascii_uppercase
        lower_chars = string.ascii_lowercase
        digit_chars = string.digits
        symbol_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"

        pool = ""
        guaranteed = []

        if use_upper:
            pool += upper_chars
            guaranteed.append(secrets.choice(upper_chars))
        if use_lower:
            pool += lower_chars
            guaranteed.append(secrets.choice(lower_chars))
        if use_digits:
            pool += digit_chars
            guaranteed.append(secrets.choice(digit_chars))
        if use_symbols:
            pool += symbol_chars
            guaranteed.append(secrets.choice(symbol_chars))

        remaining = length - len(guaranteed)
        if remaining < 0:
            guaranteed = guaranteed[:length]
            remaining = 0

        random_picks = [secrets.choice(pool) for _ in range(remaining)]
        final = guaranteed + random_picks
        secrets.SystemRandom().shuffle(final)
        return "".join(final)

    def evaluate_strength(self, password, use_upper, use_lower, use_digits, use_symbols):
        length = len(password)
        
        # Count types
        types_count = sum([use_upper, use_lower, use_digits, use_symbols])

        if length < 8 or types_count == 1:
            level = 1
            text = "Weak"
            color = THEME["weak"]
        elif length >= 12 and types_count == 4:
            level = 4
            text = "Very Strong"
            color = THEME["vstrong"]
        elif length >= 10 and types_count >= 3:
            level = 3
            text = "Strong"
            color = THEME["strong"]
        else:
            level = 2
            text = "Medium"
            color = THEME["medium"]

        self.strength_meter.set_strength(level)
        self.strength_lbl.config(text=text, fg=color)

    def copy_to_clipboard(self):
        """Append generated password string to local keyboard clipboard and show dynamic alert overlay."""
        pwd = self.password_var.get()
        if pwd in ["Select parameters...", ""]:
            return

        self.parent.clipboard_clear()
        self.parent.clipboard_append(pwd)

        # Build dynamic overlay pop-up message
        if self.notify_lbl:
            self.notify_lbl.destroy()

        self.notify_lbl = tk.Label(
            self,
            text="✓ Password Copied to Clipboard!",
            font=("Segoe UI", 9, "bold"),
            bg=THEME["vstrong"],
            fg=THEME["black"],
            pady=6
        )
        self.notify_lbl.pack(fill="x", side="bottom")
        
        # Schedule clearing message after 2.5 seconds
        self.parent.after(2500, self._clear_notification)

    def _clear_notification(self):
        if self.notify_lbl:
            self.notify_lbl.destroy()
            self.notify_lbl = None

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIPasswordGenerator(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
