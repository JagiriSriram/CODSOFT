import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

# Global Theme Palette
THEME = {
    "bg_main": "#1e1e2e",       # Deep mocha background
    "bg_sidebar": "#181825",    # Darker panel background
    "bg_card": "#252538",       # Card background
    "bg_card_hover": "#2f2f48", # Card hover background
    "fg_text": "#cdd6f4",       # Primary light text
    "fg_muted": "#89b4fa",      # Accent blue
    "fg_sub": "#7f849c",        # Secondary muted text
    "accent": "#89b4fa",        # Blue accent
    "accent_hover": "#b4befe",  # Hover blue accent
    "high_prio": "#f38ba8",     # Red
    "med_prio": "#fab387",      # Orange
    "low_prio": "#a6e3a1",      # Green
    "white": "#ffffff"
}

class ScrollableFrame(tk.Frame):
    """
    A scrollable frame using Canvas and Scrollbar.
    """
    def __init__(self, container, *args, **kwargs):
        # Set container background
        kwargs["bg"] = THEME["bg_main"]
        super().__init__(container, *args, **kwargs)

        self.canvas = tk.Canvas(self, bg=THEME["bg_main"], highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        
        self.scrollable_frame = tk.Frame(self, bg=THEME["bg_main"])
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        
        # Configure canvas window width to resize with canvas
        self.canvas.bind('<Configure>', self._on_canvas_configure)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Mouse wheel binding for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_canvas_configure(self, event):
        # Width of internal frame should match the canvas width
        self.canvas.itemconfig(self.canvas_window, width=event.width)

    def _on_mousewheel(self, event):
        # Check if the widget is visible/active to prevent scrolling other frames
        try:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")
        except tk.TclError:
            pass


class CustomCheckbox(tk.Canvas):
    """
    A premium styled Canvas-based checkbox with animation.
    """
    def __init__(self, parent, checked=False, command=None, size=24, **kwargs):
        super().__init__(parent, width=size, height=size, bg=THEME["bg_card"], 
                         highlightthickness=0, cursor="hand2", **kwargs)
        self.checked = checked
        self.command = command
        self.size = size
        self.bind("<Button-1>", self._toggle)
        self.draw()

    def draw(self):
        self.delete("all")
        margin = 3
        # Background box
        if self.checked:
            # Filled accent box
            self.create_rectangle(
                margin, margin, self.size-margin, self.size-margin,
                fill=THEME["accent"], outline="", width=0
            )
            # Draw white checkmark
            # ✓ shape lines
            x0, y0 = self.size * 0.3, self.size * 0.5
            x1, y1 = self.size * 0.45, self.size * 0.65
            x2, y2 = self.size * 0.72, self.size * 0.35
            self.create_line(x0, y0, x1, y1, fill=THEME["bg_sidebar"], width=2.5)
            self.create_line(x1, y1, x2, y2, fill=THEME["bg_sidebar"], width=2.5)
        else:
            # Outlined empty box
            self.create_rectangle(
                margin, margin, self.size-margin, self.size-margin,
                fill="", outline=THEME["fg_sub"], width=2
            )

    def _toggle(self, event):
        self.checked = not self.checked
        self.draw()
        if self.command:
            self.command(self.checked)


class TaskCard(tk.Frame):
    """
    Represent a visual card for a single task.
    """
    def __init__(self, parent, task, on_status_toggle, on_edit, on_delete, **kwargs):
        super().__init__(parent, bg=THEME["bg_card"], bd=0, highlightthickness=0, **kwargs)
        self.task = task
        self.on_status_toggle = on_status_toggle
        self.on_edit = on_edit
        self.on_delete = on_delete

        # Left priority border indicator
        prio_colors = {
            "High": THEME["high_prio"],
            "Medium": THEME["med_prio"],
            "Low": THEME["low_prio"]
        }
        indicator_color = prio_colors.get(task["priority"], THEME["fg_sub"])
        
        self.indicator = tk.Frame(self, bg=indicator_color, width=5)
        self.indicator.pack(side="left", fill="y")

        # Inside content container
        self.content = tk.Frame(self, bg=THEME["bg_card"], padx=10, pady=8)
        self.content.pack(side="left", fill="both", expand=True)

        # Checkbox & Info container
        self.top_row = tk.Frame(self.content, bg=THEME["bg_card"])
        self.top_row.pack(fill="x", expand=True)

        # Custom checkbox
        is_completed = task["status"] == "Completed"
        self.checkbox = CustomCheckbox(
            self.top_row, 
            checked=is_completed, 
            command=self._toggle_status
        )
        self.checkbox.pack(side="left", anchor="n", pady=2)

        # Text container (Title and description)
        self.text_container = tk.Frame(self.top_row, bg=THEME["bg_card"])
        self.text_container.pack(side="left", fill="x", expand=True, padx=10)

        # Title Label
        title_font = ("Segoe UI", 11, "bold" if not is_completed else "bold overstrike")
        title_fg = THEME["fg_sub"] if is_completed else THEME["white"]
        self.title_lbl = tk.Label(
            self.text_container, 
            text=task["title"], 
            font=title_font, 
            fg=title_fg, 
            bg=THEME["bg_card"], 
            anchor="w",
            justify="left",
            wraplength=450
        )
        self.title_lbl.pack(fill="x", anchor="w")

        # Description Label (if exists)
        if task["description"]:
            desc_fg = THEME["fg_sub"]
            self.desc_lbl = tk.Label(
                self.text_container, 
                text=task["description"], 
                font=("Segoe UI", 9), 
                fg=desc_fg, 
                bg=THEME["bg_card"], 
                anchor="w",
                justify="left",
                wraplength=450
            )
            self.desc_lbl.pack(fill="x", anchor="w", pady=(2, 0))

        # Bottom row metadata (Category, due date, edit/delete buttons)
        self.bottom_row = tk.Frame(self.content, bg=THEME["bg_card"])
        self.bottom_row.pack(fill="x", pady=(8, 0))

        # Category chip
        cat_frame = tk.Frame(self.bottom_row, bg="#313244", padx=6, pady=2)
        cat_frame.pack(side="left", anchor="center")
        self.cat_lbl = tk.Label(
            cat_frame, 
            text=task["category"], 
            font=("Segoe UI", 8, "bold"), 
            fg=THEME["fg_muted"], 
            bg="#313244"
        )
        self.cat_lbl.pack()

        # Due date text
        if task["due_date"]:
            due_date_str = task["due_date"]
            due_fg = THEME["fg_sub"]
            
            # Check if overdue
            try:
                due_dt = datetime.strptime(due_date_str, "%Y-%m-%d").date()
                if due_dt < datetime.now().date() and not is_completed:
                    due_fg = THEME["high_prio"]
                    due_date_str += " (Overdue)"
            except ValueError:
                pass

            self.due_lbl = tk.Label(
                self.bottom_row, 
                text=f" 📅 {due_date_str}", 
                font=("Segoe UI", 8.5), 
                fg=due_fg, 
                bg=THEME["bg_card"]
            )
            self.due_lbl.pack(side="left", padx=12, anchor="center")

        # Edit/Delete Buttons container
        self.actions_frame = tk.Frame(self.bottom_row, bg=THEME["bg_card"])
        self.actions_frame.pack(side="right", anchor="center")

        # Edit button (styled label acting as button)
        self.edit_btn = tk.Label(
            self.actions_frame, 
            text="✏️ Edit", 
            font=("Segoe UI", 9), 
            fg=THEME["fg_muted"], 
            bg=THEME["bg_card"], 
            cursor="hand2",
            padx=5
        )
        self.edit_btn.pack(side="left", padx=5)
        self.edit_btn.bind("<Button-1>", lambda e: self.on_edit(self.task))

        # Delete button
        self.del_btn = tk.Label(
            self.actions_frame, 
            text="🗑️ Delete", 
            font=("Segoe UI", 9), 
            fg=THEME["high_prio"], 
            bg=THEME["bg_card"], 
            cursor="hand2",
            padx=5
        )
        self.del_btn.pack(side="left", padx=5)
        self.del_btn.bind("<Button-1>", lambda e: self.on_delete(self.task["id"]))

        # Bind hover events to frame and text items to create visual depth
        self.bind_hover_recursive(self, THEME["bg_card_hover"])

    def _toggle_status(self, is_checked):
        status = "Completed" if is_checked else "Pending"
        # Toggle fonts immediately for responsiveness
        title_font = ("Segoe UI", 11, "bold" if is_checked else "normal")
        if is_checked:
            title_font = ("Segoe UI", 11, "bold overstrike")
            self.title_lbl.config(fg=THEME["fg_sub"], font=title_font)
        else:
            self.title_lbl.config(fg=THEME["white"], font=title_font)
            
        self.on_status_toggle(self.task["id"], status)

    def bind_hover_recursive(self, widget, hover_color):
        """Recursively bind Enter and Leave events to show smooth color changes on hover."""
        # Don't change indicator, delete button, edit button, checkbox backgrounds
        if widget not in [self.indicator, self.del_btn, self.edit_btn, self.checkbox]:
            widget.bind("<Enter>", lambda e: self.on_hover_enter(hover_color))
            widget.bind("<Leave>", lambda e: self.on_hover_leave())
        
        for child in widget.winfo_children():
            self.bind_hover_recursive(child, hover_color)

    def on_hover_enter(self, hover_color):
        self.config(bg=hover_color)
        self.content.config(bg=hover_color)
        self.top_row.config(bg=hover_color)
        self.text_container.config(bg=hover_color)
        self.title_lbl.config(bg=hover_color)
        if hasattr(self, "desc_lbl"):
            self.desc_lbl.config(bg=hover_color)
        self.bottom_row.config(bg=hover_color)
        if hasattr(self, "due_lbl"):
            self.due_lbl.config(bg=hover_color)
        self.actions_frame.config(bg=hover_color)
        self.edit_btn.config(bg=hover_color)
        self.del_btn.config(bg=hover_color)

    def on_hover_leave(self):
        normal_color = THEME["bg_card"]
        self.config(bg=normal_color)
        self.content.config(bg=normal_color)
        self.top_row.config(bg=normal_color)
        self.text_container.config(bg=normal_color)
        self.title_lbl.config(bg=normal_color)
        if hasattr(self, "desc_lbl"):
            self.desc_lbl.config(bg=normal_color)
        self.bottom_row.config(bg=normal_color)
        if hasattr(self, "due_lbl"):
            self.due_lbl.config(bg=normal_color)
        self.actions_frame.config(bg=normal_color)
        self.edit_btn.config(bg=normal_color)
        self.del_btn.config(bg=normal_color)


class TaskDialog(tk.Toplevel):
    """
    A custom modern popup window for adding or editing tasks.
    """
    def __init__(self, parent, title="Task Details", task=None, categories=None):
        super().__init__(parent)
        self.parent = parent
        self.title(title)
        self.task = task
        self.categories = categories or ["General", "Work", "Personal", "Shopping", "Health"]
        self.result = None

        # Style & geometry
        self.configure(bg=THEME["bg_main"])
        self.resizable(False, False)
        
        # Center dialog
        self.width = 450
        self.height = 420
        x = parent.winfo_x() + (parent.winfo_width() - self.width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
        
        # Make modal
        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._load_task_data()

    def _build_ui(self):
        container = tk.Frame(self, bg=THEME["bg_main"], padx=20, pady=20)
        container.pack(fill="both", expand=True)

        # Title Field
        tk.Label(container, text="Task Title*", font=("Segoe UI", 9, "bold"), fg=THEME["white"], bg=THEME["bg_main"]).pack(anchor="w", pady=(0, 2))
        self.title_entry = tk.Entry(container, font=("Segoe UI", 11), bg=THEME["bg_card"], fg=THEME["white"], insertbackground="white", bd=0, highlightthickness=1, highlightbackground=THEME["fg_sub"], highlightcolor=THEME["accent"])
        self.title_entry.pack(fill="x", pady=(0, 10), ipady=5)

        # Description Field
        tk.Label(container, text="Description", font=("Segoe UI", 9, "bold"), fg=THEME["white"], bg=THEME["bg_main"]).pack(anchor="w", pady=(0, 2))
        self.desc_text = tk.Text(container, font=("Segoe UI", 10), bg=THEME["bg_card"], fg=THEME["white"], insertbackground="white", bd=0, highlightthickness=1, highlightbackground=THEME["fg_sub"], highlightcolor=THEME["accent"], height=4)
        self.desc_text.pack(fill="x", pady=(0, 10))

        # Row with two columns: Priority and Category
        mid_row = tk.Frame(container, bg=THEME["bg_main"])
        mid_row.pack(fill="x", pady=(0, 10))

        # Priority Selection
        prio_frame = tk.Frame(mid_row, bg=THEME["bg_main"])
        prio_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        tk.Label(prio_frame, text="Priority", font=("Segoe UI", 9, "bold"), fg=THEME["white"], bg=THEME["bg_main"]).pack(anchor="w", pady=(0, 2))
        self.prio_var = tk.StringVar(value="Medium")
        self.prio_combo = ttk.Combobox(prio_frame, textvariable=self.prio_var, values=["Low", "Medium", "High"], state="readonly", font=("Segoe UI", 10))
        self.prio_combo.pack(fill="x", ipady=3)

        # Category Selection / Custom input
        cat_frame = tk.Frame(mid_row, bg=THEME["bg_main"])
        cat_frame.pack(side="right", fill="x", expand=True)
        tk.Label(cat_frame, text="Category", font=("Segoe UI", 9, "bold"), fg=THEME["white"], bg=THEME["bg_main"]).pack(anchor="w", pady=(0, 2))
        
        self.cat_var = tk.StringVar(value="General")
        self.cat_combo = ttk.Combobox(cat_frame, textvariable=self.cat_var, values=self.categories, font=("Segoe UI", 10))
        self.cat_combo.pack(fill="x", ipady=3)

        # Due Date Field (YYYY-MM-DD)
        tk.Label(container, text="Due Date (YYYY-MM-DD)", font=("Segoe UI", 9, "bold"), fg=THEME["white"], bg=THEME["bg_main"]).pack(anchor="w", pady=(0, 2))
        self.due_entry = tk.Entry(container, font=("Segoe UI", 11), bg=THEME["bg_card"], fg=THEME["white"], insertbackground="white", bd=0, highlightthickness=1, highlightbackground=THEME["fg_sub"], highlightcolor=THEME["accent"])
        self.due_entry.pack(fill="x", pady=(0, 20), ipady=5)
        # Placeholder or helper label
        self.due_helper = tk.Label(container, text="e.g. 2026-07-31 (leave empty if no due date)", font=("Segoe UI", 8), fg=THEME["fg_sub"], bg=THEME["bg_main"])
        self.due_helper.pack(anchor="w", pady=(0, 15))

        # Bottom buttons
        btn_row = tk.Frame(container, bg=THEME["bg_main"])
        btn_row.pack(fill="x", side="bottom")

        # Save Button
        save_btn = tk.Button(btn_row, text="Save Task", font=("Segoe UI", 10, "bold"), bg=THEME["accent"], fg=THEME["bg_main"], activebackground=THEME["accent_hover"], activeforeground=THEME["bg_main"], bd=0, cursor="hand2", padx=20, pady=8, command=self._save)
        save_btn.pack(side="right")

        # Cancel Button
        cancel_btn = tk.Button(btn_row, text="Cancel", font=("Segoe UI", 10), bg=THEME["bg_card"], fg=THEME["fg_text"], activebackground=THEME["bg_card_hover"], activeforeground=THEME["white"], bd=0, cursor="hand2", padx=15, pady=8, command=self.destroy)
        cancel_btn.pack(side="right", padx=10)

    def _load_task_data(self):
        if self.task:
            self.title_entry.insert(0, self.task.get("title", ""))
            self.desc_text.insert("1.0", self.task.get("description", ""))
            self.prio_var.set(self.task.get("priority", "Medium"))
            self.cat_var.set(self.task.get("category", "General"))
            self.due_entry.insert(0, self.task.get("due_date", ""))

    def _save(self):
        title = self.title_entry.get().strip()
        description = self.desc_text.get("1.0", tk.END).strip()
        priority = self.prio_var.get()
        category = self.cat_var.get().strip()
        due_date = self.due_entry.get().strip()

        # Validation
        if not title:
            messagebox.showerror("Validation Error", "Task Title is required!", parent=self)
            return

        if due_date:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Validation Error", "Due Date must be in YYYY-MM-DD format!", parent=self)
                return

        if not category:
            category = "General"

        self.result = {
            "title": title,
            "description": description,
            "priority": priority,
            "category": category,
            "due_date": due_date
        }
        self.destroy()
