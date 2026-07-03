import tkinter as tk
from tkinter import ttk, messagebox
from db_manager import DatabaseManager
from gui_components import THEME, ScrollableFrame, TaskCard, TaskDialog

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskFlow - Premium To-Do List")
        self.root.geometry("950x700")
        self.root.configure(bg=THEME["bg_main"])
        self.root.minsize(800, 600)

        # Center the window on screen
        self.center_window()

        # Initialize Database Manager
        self.db = DatabaseManager()

        # Active Filters State
        self.active_status = "All"
        self.active_category = "All"
        self.sort_by = "created_at_desc"

        # Apply ttk styles for custom dropdowns
        self.setup_ttk_styles()

        # Build Layout
        self._build_sidebar()
        self._build_main_area()

        # Initial Refresh
        self.refresh_categories()
        self.refresh_task_list()

    def center_window(self):
        self.root.update_idletasks()
        width = 950
        height = 700
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def setup_ttk_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        
        # Style Comboboxes
        style.configure(
            "TCombobox",
            fieldbackground=THEME["bg_card"],
            background=THEME["bg_sidebar"],
            foreground=THEME["white"],
            bordercolor=THEME["fg_sub"],
            arrowcolor=THEME["accent"]
        )
        style.map(
            "TCombobox",
            fieldbackground=[('readonly', THEME["bg_card"])],
            foreground=[('readonly', THEME["white"])]
        )

        # Style Scrollbar
        style.configure(
            "Vertical.TScrollbar",
            gripcount=0,
            background=THEME["bg_sidebar"],
            troughcolor=THEME["bg_main"],
            bordercolor=THEME["bg_main"],
            arrowcolor=THEME["fg_sub"]
        )

    def _build_sidebar(self):
        self.sidebar = tk.Frame(self.root, bg=THEME["bg_sidebar"], width=260)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        # App Logo & Name
        logo_frame = tk.Frame(self.sidebar, bg=THEME["bg_sidebar"], pady=25)
        logo_frame.pack(fill="x")
        
        logo_lbl = tk.Label(
            logo_frame, 
            text="⚡ TaskFlow", 
            font=("Segoe UI", 20, "bold"), 
            fg=THEME["accent"], 
            bg=THEME["bg_sidebar"]
        )
        logo_lbl.pack()

        # Quick Add Button
        add_btn = tk.Button(
            self.sidebar,
            text="➕ Add New Task",
            font=("Segoe UI", 11, "bold"),
            bg=THEME["accent"],
            fg=THEME["bg_sidebar"],
            activebackground=THEME["accent_hover"],
            activeforeground=THEME["bg_sidebar"],
            bd=0,
            cursor="hand2",
            padx=15,
            pady=10,
            command=self.open_add_task_dialog
        )
        add_btn.pack(fill="x", padx=20, pady=(0, 25))

        # Status Filter Headers/Buttons
        tk.Label(
            self.sidebar, 
            text="TASKS STATUS", 
            font=("Segoe UI", 8, "bold"), 
            fg=THEME["fg_sub"], 
            bg=THEME["bg_sidebar"]
        )
        self.sidebar_section_label_pack(tk.Label) # Pack custom tags helper

        self.status_buttons = {}
        for status in ["All", "Pending", "Completed"]:
            btn = tk.Label(
                self.sidebar,
                text=f"  {status}",
                font=("Segoe UI", 10, "bold"),
                fg=THEME["fg_text"] if status != "All" else THEME["accent"],
                bg=THEME["bg_sidebar"],
                cursor="hand2",
                anchor="w",
                pady=8
            )
            btn.pack(fill="x", padx=15)
            btn.bind("<Button-1>", lambda e, s=status: self.set_status_filter(s))
            self.status_buttons[status] = btn

        # Divider
        divider = tk.Frame(self.sidebar, bg=THEME["bg_main"], height=2)
        divider.pack(fill="x", padx=15, pady=20)

        # Categories Panel Title
        tk.Label(
            self.sidebar, 
            text="CATEGORIES", 
            font=("Segoe UI", 8, "bold"), 
            fg=THEME["fg_sub"], 
            bg=THEME["bg_sidebar"]
        ).pack(anchor="w", padx=20, pady=(0, 10))

        # Category Chips Frame
        self.cat_chips_frame = tk.Frame(self.sidebar, bg=THEME["bg_sidebar"])
        self.cat_chips_frame.pack(fill="both", expand=True, padx=15)

    def sidebar_section_label_pack(self, widget_class):
        # Helper to pack labels with correct padding in the sidebar
        for child in self.sidebar.winfo_children():
            if isinstance(child, widget_class) and child.cget("text") == "TASKS STATUS":
                child.pack(anchor="w", padx=20, pady=(0, 10))

    def _build_main_area(self):
        self.main_area = tk.Frame(self.root, bg=THEME["bg_main"])
        self.main_area.pack(side="right", fill="both", expand=True)

        # Header Frame (Search and Sort Controls)
        header = tk.Frame(self.main_area, bg=THEME["bg_main"], padx=25, pady=20)
        header.pack(fill="x")

        # Search Bar Container
        search_container = tk.Frame(header, bg=THEME["bg_card"], padx=10, pady=5, bd=0, highlightthickness=1, highlightbackground=THEME["fg_sub"], highlightcolor=THEME["accent"])
        search_container.pack(side="left", fill="x", expand=True, pright=15) # Wait, let's fix packing options
        search_container.pack(side="left", fill="x", expand=True, padx=(0, 15))

        search_icon = tk.Label(search_container, text="🔍", font=("Segoe UI", 11), fg=THEME["fg_sub"], bg=THEME["bg_card"])
        search_icon.pack(side="left")

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_task_list())
        
        self.search_entry = tk.Entry(
            search_container, 
            textvariable=self.search_var, 
            font=("Segoe UI", 11), 
            bg=THEME["bg_card"], 
            fg=THEME["white"], 
            bd=0, 
            insertbackground="white", 
            highlightthickness=0
        )
        self.search_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Sort Frame
        sort_frame = tk.Frame(header, bg=THEME["bg_main"])
        sort_frame.pack(side="right")

        tk.Label(sort_frame, text="Sort by: ", font=("Segoe UI", 10), fg=THEME["fg_text"], bg=THEME["bg_main"]).pack(side="left")
        
        self.sort_var = tk.StringVar(value="created_at_desc")
        self.sort_combo = ttk.Combobox(
            sort_frame, 
            textvariable=self.sort_var, 
            values=[
                ("Newest First", "created_at_desc"), 
                ("Due Date (Asc)", "due_date_asc"), 
                ("Due Date (Desc)", "due_date_desc"),
                ("Priority (High to Low)", "priority_high_first")
            ], 
            state="readonly",
            width=20
        )
        self.sort_combo.pack(side="left")
        self.sort_combo.bind("<<ComboboxSelected>>", self.on_sort_changed)
        
        # Override the display text mapped values for display mapping
        self.sort_display_map = {
            "Newest First": "created_at_desc",
            "Due Date (Asc)": "due_date_asc",
            "Due Date (Desc)": "due_date_desc",
            "Priority (High to Low)": "priority_high_first"
        }
        self.sort_combo.configure(values=list(self.sort_display_map.keys()))
        self.sort_combo.set("Newest First")

        # Scrollable Tasks list
        self.tasks_container = ScrollableFrame(self.main_area)
        self.tasks_container.pack(fill="both", expand=True, padx=25, pady=(0, 20))

        # Bottom Stats Bar
        self.stats_bar = tk.Frame(self.main_area, bg=THEME["bg_sidebar"], height=40, padx=25)
        self.stats_bar.pack(fill="x", side="bottom")

        self.stats_lbl = tk.Label(
            self.stats_bar,
            text="Pending: 0  |  Completed: 0",
            font=("Segoe UI", 9.5, "bold"),
            fg=THEME["fg_sub"],
            bg=THEME["bg_sidebar"]
        )
        self.stats_lbl.pack(side="left", fill="y")
        
        copyright_lbl = tk.Label(
            self.stats_bar,
            text="TaskFlow CLI-GUI v1.0",
            font=("Segoe UI", 8.5),
            fg=THEME["fg_sub"],
            bg=THEME["bg_sidebar"]
        )
        copyright_lbl.pack(side="right", fill="y")

    def on_sort_changed(self, event):
        selected_disp = self.sort_combo.get()
        self.sort_by = self.sort_display_map.get(selected_disp, "created_at_desc")
        self.refresh_task_list()

    def set_status_filter(self, status):
        # Reset previous buttons colors
        for s, btn in self.status_buttons.items():
            btn.config(fg=THEME["fg_text"])
        
        # Set active button color
        self.status_buttons[status].config(fg=THEME["accent"])
        self.active_status = status
        self.refresh_task_list()

    def set_category_filter(self, category):
        self.active_category = category
        self.refresh_categories() # Re-render category chips to show highlight
        self.refresh_task_list()

    def refresh_categories(self):
        # Clear existing category chips
        for child in self.cat_chips_frame.winfo_children():
            child.destroy()

        categories = self.db.get_categories()
        all_tasks = self.db.get_tasks()
        
        # Render "All" Category Chip
        all_count = len(all_tasks)
        self._create_category_chip("All", all_count, self.active_category == "All")

        # Render custom category chips
        for cat in categories:
            # Count items in this category
            count = sum(1 for t in all_tasks if t["category"] == cat)
            self._create_category_chip(cat, count, self.active_category == cat)

    def _create_category_chip(self, category, count, is_active):
        chip_bg = THEME["accent"] if is_active else THEME["bg_card"]
        chip_fg = THEME["bg_main"] if is_active else THEME["fg_text"]
        
        chip = tk.Frame(self.cat_chips_frame, bg=chip_bg, padx=10, pady=5)
        chip.pack(fill="x", pady=4)
        
        lbl = tk.Label(
            chip, 
            text=f"{category}", 
            font=("Segoe UI", 9.5, "bold" if is_active else "normal"), 
            fg=chip_fg, 
            bg=chip_bg,
            anchor="w",
            cursor="hand2"
        )
        lbl.pack(side="left", fill="x", expand=True)

        cnt_lbl = tk.Label(
            chip, 
            text=f"{count}", 
            font=("Segoe UI", 8.5, "bold"), 
            fg=chip_fg, 
            bg=chip_bg,
            cursor="hand2"
        )
        cnt_lbl.pack(side="right")

        # Click event handlers
        for widget in [chip, lbl, cnt_lbl]:
            widget.bind("<Button-1>", lambda e, c=category: self.set_category_filter(c))

    def refresh_task_list(self):
        # Get scrolled frame inner frame
        scroll_frame = self.tasks_container.scrollable_frame

        # Clear active task cards
        for child in scroll_frame.winfo_children():
            child.destroy()

        # Query Database with current filters
        search = self.search_var.get().strip()
        tasks = self.db.get_tasks(
            search_query=search,
            status_filter=self.active_status,
            category_filter=self.active_category,
            sort_by=self.sort_by
        )

        # Update Stats Bar
        all_tasks = self.db.get_tasks()
        pending_count = sum(1 for t in all_tasks if t["status"] == "Pending")
        completed_count = sum(1 for t in all_tasks if t["status"] == "Completed")
        self.stats_lbl.config(text=f"Pending Tasks: {pending_count}   |   Completed Tasks: {completed_count}")

        if not tasks:
            empty_lbl = tk.Label(
                scroll_frame,
                text="🎉 No tasks found! Create a new task to get started.",
                font=("Segoe UI", 12),
                fg=THEME["fg_sub"],
                bg=THEME["bg_main"],
                pady=60
            )
            empty_lbl.pack(fill="x")
            return

        # Render Task Cards
        for task in tasks:
            card = TaskCard(
                scroll_frame,
                task=task,
                on_status_toggle=self.on_task_status_toggle,
                on_edit=self.open_edit_task_dialog,
                on_delete=self.delete_task
            )
            card.pack(fill="x", pady=6)

    def on_task_status_toggle(self, task_id, new_status):
        self.db.update_status(task_id, new_status)
        self.refresh_categories()
        # Delay list refresh slightly to give database update time and checkbox animation visibility
        self.root.after(100, self.refresh_task_list)

    def open_add_task_dialog(self):
        categories = self.db.get_categories()
        dialog = TaskDialog(self.root, title="➕ Create New Task", categories=categories)
        self.root.wait_window(dialog)
        
        if dialog.result:
            self.db.add_task(
                title=dialog.result["title"],
                description=dialog.result["description"],
                priority=dialog.result["priority"],
                category=dialog.result["category"],
                due_date=dialog.result["due_date"]
            )
            self.refresh_categories()
            self.refresh_task_list()

    def open_edit_task_dialog(self, task):
        categories = self.db.get_categories()
        dialog = TaskDialog(self.root, title="✏️ Edit Task Details", task=task, categories=categories)
        self.root.wait_window(dialog)

        if dialog.result:
            self.db.update_task(
                task_id=task["id"],
                title=dialog.result["title"],
                description=dialog.result["description"],
                priority=dialog.result["priority"],
                category=dialog.result["category"],
                due_date=dialog.result["due_date"],
                status=task["status"]
            )
            self.refresh_categories()
            self.refresh_task_list()

    def delete_task(self, task_id):
        confirm = messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this task?", parent=self.root)
        if confirm:
            self.db.delete_task(task_id)
            self.refresh_categories()
            self.refresh_task_list()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()
