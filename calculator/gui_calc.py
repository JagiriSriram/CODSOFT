import tkinter as tk
from tkinter import ttk, messagebox

# Theme Palette (Consistent with TaskFlow UI)
THEME = {
    "bg_main": "#1e1e2e",       # Deep mocha background
    "bg_display": "#181825",    # Darker background for display
    "bg_btn_digit": "#252538",  # Digit button base
    "bg_btn_digit_h": "#313244",# Digit button hover
    "bg_btn_op": "#313244",     # Operator button base
    "bg_btn_op_h": "#45475a",   # Operator button hover
    "bg_btn_accent": "#89b4fa", # Equal/Highlight button base
    "bg_btn_accent_h": "#b4befe",# Equal/Highlight button hover
    "bg_btn_danger": "#f38ba8", # Clear/Delete button base
    "bg_btn_danger_h": "#f5e0dc",# Clear/Delete button hover
    "fg_text": "#cdd6f4",       # Normal text
    "fg_sub": "#7f849c",        # Secondary text
    "white": "#ffffff",
    "black": "#11111b"
}

class HoverButton(tk.Button):
    """A standard button styled with custom hover animations."""
    def __init__(self, parent, hover_bg, normal_bg, *args, **kwargs):
        super().__init__(parent, bg=normal_bg, activebackground=hover_bg, bd=0, relief="flat", **kwargs)
        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.bind("<Enter>", lambda e: self.config(bg=self.hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self.normal_bg))


class GUICalculator(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, bg=THEME["bg_main"], **kwargs)
        self.parent = parent
        self.parent.title("Calculator")
        self.parent.geometry("380x560")
        self.parent.resizable(False, False)
        self.parent.configure(bg=THEME["bg_main"])

        self.expression = ""
        self.history = []
        self.history_expanded = False

        self._build_ui()
        self._bind_keys()

    def _build_ui(self):
        # Master grid setup
        self.pack(fill="both", expand=True)

        # Top Display Area (Equation & Entry)
        self.display_frame = tk.Frame(self, bg=THEME["bg_display"], height=120, bd=0)
        self.display_frame.pack(fill="x", side="top")
        self.display_frame.pack_propagate(False)

        # History toggle button (small, top-left on display)
        self.hist_btn = HoverButton(
            self.display_frame,
            hover_bg=THEME["bg_btn_op_h"],
            normal_bg=THEME["bg_display"],
            text="📜 History",
            font=("Segoe UI", 9, "bold"),
            fg=THEME["fg_muted"] if "fg_muted" in THEME else THEME["fg_sub"],
            cursor="hand2",
            padx=10,
            command=self.toggle_history
        )
        self.hist_btn.pack(anchor="w", padx=10, pady=5)

        # Equation Label (shows building expression)
        self.equation_lbl = tk.Label(
            self.display_frame,
            text="",
            font=("Segoe UI", 11),
            fg=THEME["fg_sub"],
            bg=THEME["bg_display"],
            anchor="e",
            padx=15
        )
        self.equation_lbl.pack(fill="x", side="top", pady=(5, 0))

        # Result Entry Display (shows current typed number / total)
        self.result_lbl = tk.Label(
            self.display_frame,
            text="0",
            font=("Segoe UI", 24, "bold"),
            fg=THEME["white"],
            bg=THEME["bg_display"],
            anchor="e",
            padx=15
        )
        self.result_lbl.pack(fill="x", side="top", pady=5)

        # Keypad Grid Panel
        self.keypad_frame = tk.Frame(self, bg=THEME["bg_main"], padx=10, pady=10)
        self.keypad_frame.pack(fill="both", expand=True)

        # Grid weights setup
        for r in range(5):
            self.keypad_frame.rowconfigure(r, weight=1, uniform="equal")
        for c in range(4):
            self.keypad_frame.columnconfigure(c, weight=1, uniform="equal")

        # Button Layout definition
        # (Text, Row, Col, Columnspan, Button type)
        buttons_layout = [
            # Row 0
            ("C",   0, 0, 1, "danger"),
            ("^",   0, 1, 1, "op"),
            ("%",   0, 2, 1, "op"),
            ("⌫",   0, 3, 1, "danger"),
            # Row 1
            ("7",   1, 0, 1, "digit"),
            ("8",   1, 1, 1, "digit"),
            ("9",   1, 2, 1, "digit"),
            ("÷",   1, 3, 1, "op"),
            # Row 2
            ("4",   2, 0, 1, "digit"),
            ("5",   2, 1, 1, "digit"),
            ("6",   2, 2, 1, "digit"),
            ("×",   2, 3, 1, "op"),
            # Row 3
            ("1",   3, 0, 1, "digit"),
            ("2",   3, 1, 1, "digit"),
            ("3",   3, 2, 1, "digit"),
            ("-",   3, 3, 1, "op"),
            # Row 4
            ("0",   4, 0, 1, "digit"),
            (".",   4, 1, 1, "digit"),
            ("=",   4, 2, 1, "accent"),
            ("+",   4, 3, 1, "op")
        ]

        for text, r, c, cspan, btype in buttons_layout:
            self._create_button(text, r, c, cspan, btype)

        # Right-side History Listbox Container (hidden by default)
        self.history_frame = tk.Frame(self, bg=THEME["bg_display"], width=240, padx=10, pady=10)
        # Packed only when toggled

        hist_title_row = tk.Frame(self.history_frame, bg=THEME["bg_display"])
        hist_title_row.pack(fill="x", pady=(0, 10))

        tk.Label(
            hist_title_row,
            text="History",
            font=("Segoe UI", 11, "bold"),
            fg=THEME["white"],
            bg=THEME["bg_display"]
        ).pack(side="left")

        clear_hist_btn = HoverButton(
            hist_title_row,
            hover_bg=THEME["bg_btn_danger"],
            normal_bg="#313244",
            text="Clear",
            font=("Segoe UI", 8, "bold"),
            fg=THEME["white"],
            padx=8,
            command=self.clear_history_log
        )
        clear_hist_btn.pack(side="right")

        # Scrollbar and Listbox for history logs
        self.hist_scroll = ttk.Scrollbar(self.history_frame, orient="vertical")
        
        # Style listbox with dark background matching the display
        self.hist_listbox = tk.Listbox(
            self.history_frame,
            font=("Segoe UI", 9),
            bg=THEME["bg_main"],
            fg=THEME["fg_text"],
            selectbackground=THEME["bg_btn_op_h"],
            selectforeground=THEME["white"],
            bd=0,
            highlightthickness=0,
            yscrollcommand=self.hist_scroll.set
        )
        self.hist_scroll.config(command=self.hist_listbox.yview)
        
        self.hist_scroll.pack(side="right", fill="y")
        self.hist_listbox.pack(side="left", fill="both", expand=True)
        self.hist_listbox.bind("<Double-1>", self.load_history_item)

    def _create_button(self, text, r, c, cspan, btype):
        """Build and style buttons based on type and layout positions."""
        btn_fonts = ("Segoe UI", 14, "bold")
        
        if btype == "digit":
            bg = THEME["bg_btn_digit"]
            bg_h = THEME["bg_btn_digit_h"]
            fg = THEME["fg_text"]
        elif btype == "op":
            bg = THEME["bg_btn_op"]
            bg_h = THEME["bg_btn_op_h"]
            fg = THEME["accent"] if "accent" in THEME else THEME["fg_sub"]
        elif btype == "accent":
            bg = THEME["bg_btn_accent"]
            bg_h = THEME["bg_btn_accent_h"]
            fg = THEME["black"]
            btn_fonts = ("Segoe UI", 16, "bold")
        else: # danger (C/DEL)
            bg = THEME["bg_btn_danger"]
            bg_h = THEME["bg_btn_danger_h"]
            fg = THEME["black"]

        btn = HoverButton(
            self.keypad_frame,
            hover_bg=bg_h,
            normal_bg=bg,
            text=text,
            font=btn_fonts,
            fg=fg,
            cursor="hand2",
            command=lambda: self.on_button_click(text)
        )
        btn.grid(row=r, column=c, columnspan=cspan, sticky="nsew", padx=4, pady=4)

    def _bind_keys(self):
        """Binds keyboard inputs to calculator commands."""
        for num in range(10):
            self.parent.bind(str(num), lambda e, n=num: self.on_button_click(str(n)))
        
        # Operators
        self.parent.bind("+", lambda e: self.on_button_click("+"))
        self.parent.bind("-", lambda e: self.on_button_click("-"))
        self.parent.bind("*", lambda e: self.on_button_click("×"))
        self.parent.bind("/", lambda e: self.on_button_click("÷"))
        self.parent.bind("%", lambda e: self.on_button_click("%"))
        self.parent.bind("^", lambda e: self.on_button_click("^"))
        self.parent.bind(".", lambda e: self.on_button_click("."))
        
        # Actions
        self.parent.bind("<Return>", lambda e: self.on_button_click("="))
        self.parent.bind("<BackSpace>", lambda e: self.on_button_click("⌫"))
        self.parent.bind("<Escape>", lambda e: self.on_button_click("C"))

    def toggle_history(self):
        """Sliding logic: expands or collapses window geometry to reveal history log."""
        if self.history_expanded:
            self.history_frame.pack_forget()
            self.parent.geometry("380x560")
            self.hist_btn.config(text="📜 History")
        else:
            self.parent.geometry("620x560")
            self.history_frame.pack(side="right", fill="y", before=self.display_frame) # Put sidebar on the right
            self.history_frame.pack_propagate(False)
            self.hist_btn.config(text="◀ Close")
            
        self.history_expanded = not self.history_expanded

    def update_history_listbox(self):
        self.hist_listbox.delete(0, tk.END)
        for item in reversed(self.history):
            self.hist_listbox.insert(tk.END, item)

    def clear_history_log(self):
        self.history.clear()
        self.update_history_listbox()

    def load_history_item(self, event):
        """Load double-clicked history result into display."""
        selection = self.hist_listbox.curselection()
        if selection:
            item = self.hist_listbox.get(selection[0])
            # Item format: "12 + 5 = 17" -> extract result part after "="
            if " = " in item:
                result_part = item.split(" = ")[1].strip()
                self.expression = result_part
                self.result_lbl.config(text=result_part)
                self.equation_lbl.config(text="")

    def on_button_click(self, char):
        if char == "C":
            self.expression = ""
            self.result_lbl.config(text="0")
            self.equation_lbl.config(text="")
        elif char == "⌫":
            self.expression = self.expression[:-1]
            self.result_lbl.config(text=self.expression if self.expression else "0")
        elif char == "=":
            if not self.expression:
                return
            
            # Evaluate expression
            original_expr = self.expression
            eval_expr = self.expression.replace("×", "*").replace("÷", "/").replace("^", "**")

            # Basic syntax character sanitization
            allowed_chars = set("0123456789+-*/.%() ")
            if not all(c in allowed_chars for c in eval_expr):
                self.result_lbl.config(text="Syntax Error")
                self.expression = ""
                return

            try:
                # Calculate
                res = eval(eval_expr, {"__builtins__": None}, {})
                
                # Format floating output cleanly
                if isinstance(res, float) and res.is_integer():
                    res_str = str(int(res))
                elif isinstance(res, float):
                    res_str = f"{res:.8f}".rstrip('0').rstrip('.')
                else:
                    res_str = str(res)

                # Show on display
                self.result_lbl.config(text=res_str)
                self.equation_lbl.config(text=f"{original_expr} =")
                
                # Append to history logs
                self.history.append(f"{original_expr} = {res_str}")
                self.update_history_listbox()
                
                self.expression = res_str
            except ZeroDivisionError:
                self.result_lbl.config(text="Div by Zero")
                self.expression = ""
            except OverflowError:
                self.result_lbl.config(text="Overflow Error")
                self.expression = ""
            except Exception:
                self.result_lbl.config(text="Syntax Error")
                self.expression = ""
        else:
            # Prevent leading multiple zeroes
            if self.expression == "0" and char in "0123456789":
                self.expression = char
            # Prevent multiple decimals in a single number sequence
            elif char == ".":
                # Splitting by operators to locate the last numerical segment
                segments = self.expression.replace("+", " ").replace("-", " ").replace("×", " ").replace("÷", " ").replace("%", " ").replace("^", " ").split()
                if segments and "." in segments[-1]:
                    return  # ignore dot click
                elif not self.expression or self.expression[-1] in "+-×÷%^":
                    self.expression += "0."
                else:
                    self.expression += "."
            else:
                # Prevent consecutive operators
                if char in "+-×÷%^" and self.expression and self.expression[-1] in "+-×÷%^":
                    # Swap operator instead of appending
                    self.expression = self.expression[:-1] + char
                elif char in "+-×÷%^" and not self.expression:
                    if char == "-":
                        self.expression = "-"
                    else:
                        return # ignore other leading operators
                else:
                    self.expression += char

            self.result_lbl.config(text=self.expression)

if __name__ == "__main__":
    root = tk.Tk()
    app = GUICalculator(root)
    root.mainloop()
