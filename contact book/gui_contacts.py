import tkinter as tk
from tkinter import ttk, messagebox
from db_contacts import ContactDatabase

# Theme Palette (Consistent with other tasks)
THEME = {
    "bg_main": "#1e1e2e",       # Deep mocha background
    "bg_sidebar": "#181825",    # Dark sidebar background
    "bg_card": "#252538",       # Selection details card
    "bg_card_hover": "#2f2f48", # Hover highlights
    "fg_text": "#cdd6f4",       # Primary light text
    "fg_sub": "#7f849c",        # Secondary muted text
    "accent": "#89b4fa",        # Blue accent
    "accent_hover": "#b4befe",  # Hover blue
    "white": "#ffffff",
    "black": "#11111b",
    "danger": "#f38ba8",        # Red
    "danger_hover": "#f5e0dc"   # Light red
}

class HoverButton(tk.Button):
    """Custom flat button with active state hover colors."""
    def __init__(self, parent, hover_bg, normal_bg, *args, **kwargs):
        super().__init__(parent, bg=normal_bg, activebackground=hover_bg, bd=0, relief="flat", **kwargs)
        self.normal_bg = normal_bg
        self.hover_bg = hover_bg
        self.bind("<Enter>", lambda e: self.config(bg=self.hover_bg))
        self.bind("<Leave>", lambda e: self.config(bg=self.normal_bg))


class AvatarCanvas(tk.Canvas):
    """Draws a visual round circle profile placeholder with name initials."""
    def __init__(self, parent, size=80, **kwargs):
        super().__init__(parent, width=size, height=size, bg=THEME["bg_card"], 
                         highlightthickness=0, **kwargs)
        self.size = size
        self.draw_avatar("?")

    def draw_avatar(self, initials):
        self.delete("all")
        margin = 2
        # Outer circle
        self.create_oval(
            margin, margin, self.size-margin, self.size-margin,
            fill=THEME["accent"], outline="", width=0
        )
        # Initials Text
        self.create_text(
            self.size // 2, self.size // 2,
            text=initials.upper(),
            font=("Segoe UI", 24, "bold"),
            fill=THEME["black"]
        )


class ContactDialog(tk.Toplevel):
    """Modal popup dialog for adding or editing contact records."""
    def __init__(self, parent, title="Contact Details", contact=None):
        super().__init__(parent)
        self.parent = parent
        self.title(title)
        self.contact = contact
        self.result = None

        self.configure(bg=THEME["bg_main"])
        self.resizable(False, False)

        # Center Dialog
        self.width = 420
        self.height = 440
        x = parent.winfo_x() + (parent.winfo_width() - self.width) // 2
        y = parent.winfo_y() + (parent.winfo_height() - self.height) // 2
        self.geometry(f"{self.width}x{self.height}+{x}+{y}")

        self.transient(parent)
        self.grab_set()

        self._build_ui()
        self._load_contact_data()

    def _build_ui(self):
        container = tk.Frame(self, bg=THEME["bg_main"], padx=20, pady=20)
        container.pack(fill="both", expand=True)

        # Name Input
        tk.Label(container, text="Name*", font=("Segoe UI", 9, "bold"), fg=THEME["white"], bg=THEME["bg_main"]).pack(anchor="w", pady=(0, 2))
        self.name_entry = tk.Entry(container, font=("Segoe UI", 11), bg=THEME["bg_card"], fg=THEME["white"], insertbackground="white", bd=0, highlightthickness=1, highlightbackground=THEME["fg_sub"], highlightcolor=THEME["accent"])
        self.name_entry.pack(fill="x", pady=(0, 15), ipady=4)

        # Phone Input
        tk.Label(container, text="Phone Number*", font=("Segoe UI", 9, "bold"), fg=THEME["white"], bg=THEME["bg_main"]).pack(anchor="w", pady=(0, 2))
        self.phone_entry = tk.Entry(container, font=("Segoe UI", 11), bg=THEME["bg_card"], fg=THEME["white"], insertbackground="white", bd=0, highlightthickness=1, highlightbackground=THEME["fg_sub"], highlightcolor=THEME["accent"])
        self.phone_entry.pack(fill="x", pady=(0, 15), ipady=4)

        # Email Input
        tk.Label(container, text="Email Address", font=("Segoe UI", 9, "bold"), fg=THEME["white"], bg=THEME["bg_main"]).pack(anchor="w", pady=(0, 2))
        self.email_entry = tk.Entry(container, font=("Segoe UI", 11), bg=THEME["bg_card"], fg=THEME["white"], insertbackground="white", bd=0, highlightthickness=1, highlightbackground=THEME["fg_sub"], highlightcolor=THEME["accent"])
        self.email_entry.pack(fill="x", pady=(0, 15), ipady=4)

        # Address Input (Text Field)
        tk.Label(container, text="Address", font=("Segoe UI", 9, "bold"), fg=THEME["white"], bg=THEME["bg_main"]).pack(anchor="w", pady=(0, 2))
        self.address_text = tk.Text(container, font=("Segoe UI", 10), bg=THEME["bg_card"], fg=THEME["white"], insertbackground="white", bd=0, highlightthickness=1, highlightbackground=THEME["fg_sub"], highlightcolor=THEME["accent"], height=3)
        self.address_text.pack(fill="x", pady=(0, 20))

        # Bottom Buttons
        btn_row = tk.Frame(container, bg=THEME["bg_main"])
        btn_row.pack(fill="x", side="bottom")

        save_btn = tk.Button(
            btn_row, 
            text="Save Contact", 
            font=("Segoe UI", 10, "bold"), 
            bg=THEME["accent"], 
            fg=THEME["black"], 
            activebackground=THEME["accent_hover"], 
            activeforeground=THEME["black"], 
            bd=0, 
            cursor="hand2", 
            padx=20, 
            pady=8,
            command=self._save
        )
        save_btn.pack(side="right")

        cancel_btn = tk.Button(
            btn_row, 
            text="Cancel", 
            font=("Segoe UI", 10), 
            bg=THEME["bg_card"], 
            fg=THEME["fg_text"], 
            activebackground=THEME["bg_card_hover"], 
            activeforeground=THEME["white"], 
            bd=0, 
            cursor="hand2", 
            padx=15, 
            pady=8,
            command=self.destroy
        )
        cancel_btn.pack(side="right", padx=10)

    def _load_contact_data(self):
        if self.contact:
            self.name_entry.insert(0, self.contact.get("name", ""))
            self.phone_entry.insert(0, self.contact.get("phone", ""))
            self.email_entry.insert(0, self.contact.get("email", ""))
            self.address_text.insert("1.0", self.contact.get("address", ""))

    def _save(self):
        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()
        address = self.address_text.get("1.0", tk.END).strip()

        if not name:
            messagebox.showerror("Validation Error", "Name is a required field!", parent=self)
            return

        if not phone:
            messagebox.showerror("Validation Error", "Phone Number is a required field!", parent=self)
            return

        self.result = {
            "name": name,
            "phone": phone,
            "email": email,
            "address": address
        }
        self.destroy()


class GUIContacts(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, bg=THEME["bg_main"], **kwargs)
        self.parent = parent
        self.parent.title("Contact Book")
        self.parent.geometry("820x600")
        self.parent.resizable(False, False)
        self.parent.configure(bg=THEME["bg_main"])

        # Setup database
        self.db = ContactDatabase()
        
        # Selected Contact state
        self.selected_contact_id = None
        self.contacts_list_data = []

        self.center_window()
        self._build_ui()
        self.refresh_contact_list()

    def center_window(self):
        self.parent.update_idletasks()
        width = 820
        height = 600
        x = (self.parent.winfo_screenwidth() // 2) - (width // 2)
        y = (self.parent.winfo_screenheight() // 2) - (height // 2)
        self.parent.geometry(f"{width}x{height}+{x}+{y}")

    def _build_ui(self):
        # 1. Left Sidebar Panel (Contacts Lists & Searches)
        sidebar = tk.Frame(self, bg=THEME["bg_sidebar"], width=320)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        # Search Box Container
        search_frame = tk.Frame(sidebar, bg=THEME["bg_card"], padx=10, pady=5, bd=0, highlightthickness=1, highlightbackground=THEME["fg_sub"], highlightcolor=THEME["accent"])
        search_frame.pack(fill="x", padx=15, pady=15)

        tk.Label(search_frame, text="🔍", font=("Segoe UI", 11), fg=THEME["fg_sub"], bg=THEME["bg_card"]).pack(side="left")
        
        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self.refresh_contact_list())
        
        search_entry = tk.Entry(
            search_frame, 
            textvariable=self.search_var, 
            font=("Segoe UI", 10), 
            bg=THEME["bg_card"], 
            fg=THEME["white"], 
            bd=0, 
            insertbackground="white", 
            highlightthickness=0
        )
        search_entry.pack(side="left", fill="x", expand=True, padx=5)

        # Contact List listbox and Scrollbar
        list_container = tk.Frame(sidebar, bg=THEME["bg_sidebar"])
        list_container.pack(fill="both", expand=True, padx=15)

        list_scroll = ttk.Scrollbar(list_container, orient="vertical")
        
        self.listbox = tk.Listbox(
            list_container,
            font=("Segoe UI", 10),
            bg=THEME["bg_card"],
            fg=THEME["fg_text"],
            selectbackground=THEME["accent"],
            selectforeground=THEME["black"],
            bd=0,
            highlightthickness=0,
            yscrollcommand=list_scroll.set
        )
        list_scroll.config(command=self.listbox.yview)
        
        list_scroll.pack(side="right", fill="y")
        self.listbox.pack(side="left", fill="both", expand=True)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        # Add Contact Button
        add_btn = HoverButton(
            sidebar,
            hover_bg=THEME["accent_hover"],
            normal_bg=THEME["accent"],
            text="➕ Add New Contact",
            font=("Segoe UI", 10, "bold"),
            fg=THEME["black"],
            cursor="hand2",
            pady=10,
            command=self.open_add_dialog
        )
        add_btn.pack(fill="x", padx=15, pady=15)

        # 2. Right Details Panel (Packs details card)
        self.detail_area = tk.Frame(self, bg=THEME["bg_main"], padx=20, pady=20)
        self.detail_area.pack(side="right", fill="both", expand=True)

        # Placeholder Label (When no selection made)
        self.placeholder_lbl = tk.Label(
            self.detail_area,
            text="📂 Select a contact from the list\nto view detailed information.",
            font=("Segoe UI", 12),
            fg=THEME["fg_sub"],
            bg=THEME["bg_main"],
            pady=100
        )
        self.placeholder_lbl.pack(fill="both", expand=True)

        # Detailed Card Frame (Hidden by default, packed on select)
        self.details_card = tk.Frame(self.detail_area, bg=THEME["bg_card"], padx=25, pady=25)

        # Card Row 1: Profile Avatar initials & Header Title
        self.profile_row = tk.Frame(self.details_card, bg=THEME["bg_card"])
        self.profile_row.pack(fill="x", pady=(0, 20))

        self.avatar = AvatarCanvas(self.profile_row, size=75)
        self.avatar.pack(side="left", padx=(0, 15))

        self.details_name_lbl = tk.Label(
            self.profile_row,
            text="Contact Name",
            font=("Segoe UI", 16, "bold"),
            fg=THEME["white"],
            bg=THEME["bg_card"],
            anchor="w"
        )
        self.details_name_lbl.pack(side="left", fill="x", expand=True)

        # Divider
        div = tk.Frame(self.details_card, bg="#313244", height=1)
        div.pack(fill="x", pady=(0, 20))

        # Details Grid layout
        self.info_grid = tk.Frame(self.details_card, bg=THEME["bg_card"])
        self.info_grid.pack(fill="both", expand=True)
        self.info_grid.columnconfigure(0, minsize=100)

        # Phone detail
        tk.Label(self.info_grid, text="📞 Phone:", font=("Segoe UI", 10, "bold"), fg=THEME["fg_sub"], bg=THEME["bg_card"], anchor="w").grid(row=0, column=0, sticky="w", pady=10)
        self.details_phone_lbl = tk.Label(self.info_grid, text="Phone text", font=("Segoe UI", 11), fg=THEME["fg_text"], bg=THEME["bg_card"], anchor="w")
        self.details_phone_lbl.grid(row=0, column=1, sticky="w", pady=10)

        # Email detail
        tk.Label(self.info_grid, text="📧 Email:", font=("Segoe UI", 10, "bold"), fg=THEME["fg_sub"], bg=THEME["bg_card"], anchor="w").grid(row=1, column=0, sticky="w", pady=10)
        self.details_email_lbl = tk.Label(self.info_grid, text="Email text", font=("Segoe UI", 11), fg=THEME["fg_text"], bg=THEME["bg_card"], anchor="w")
        self.details_email_lbl.grid(row=1, column=1, sticky="w", pady=10)

        # Address detail
        tk.Label(self.info_grid, text="🏠 Address:", font=("Segoe UI", 10, "bold"), fg=THEME["fg_sub"], bg=THEME["bg_card"], anchor="w").grid(row=2, column=0, sticky="w", pady=10)
        self.details_address_lbl = tk.Label(self.info_grid, text="Address text", font=("Segoe UI", 11), fg=THEME["fg_text"], bg=THEME["bg_card"], anchor="w", justify="left", wraplength=300)
        self.details_address_lbl.grid(row=2, column=1, sticky="w", pady=10)

        # Card Footer Action Buttons
        self.actions_row = tk.Frame(self.details_card, bg=THEME["bg_card"])
        self.actions_row.pack(fill="x", side="bottom", pady=(20, 0))

        # Edit button
        self.edit_btn = HoverButton(
            self.actions_row,
            hover_bg=THEME["bg_card_hover"],
            normal_bg="#313244",
            text="✏️ Edit Details",
            font=("Segoe UI", 10, "bold"),
            fg=THEME["accent"],
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.open_edit_dialog
        )
        self.edit_btn.pack(side="left")

        # Delete button
        self.delete_btn = HoverButton(
            self.actions_row,
            hover_bg=THEME["danger_hover"],
            normal_bg=THEME["danger"],
            text="🗑️ Delete Contact",
            font=("Segoe UI", 10, "bold"),
            fg=THEME["black"],
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.delete_current_contact
        )
        self.delete_btn.pack(side="right")

    def refresh_contact_list(self):
        """Loads contacts from SQLite and repopulates the listbox using search criteria."""
        self.listbox.delete(0, tk.END)
        query = self.search_var.get().strip()
        
        self.contacts_list_data = self.db.get_contacts(search_query=query)
        
        for c in self.contacts_list_data:
            self.listbox.insert(tk.END, f"{c['name']} ({c['phone']})")

    def on_listbox_select(self, event):
        """Callback when selecting items in the listbox. Shows the detail card panel."""
        selection = self.listbox.curselection()
        if not selection:
            return

        index = selection[0]
        # Fetch corresponding contact structure from index
        if index < len(self.contacts_list_data):
            contact = self.contacts_list_data[index]
            self.selected_contact_id = contact["id"]
            self.load_detailed_contact(contact)

    def load_detailed_contact(self, contact):
        """Display select contact information on the right-side card."""
        # Unpack placeholder and pack detailed card
        self.placeholder_lbl.pack_forget()
        self.details_card.pack(fill="both", expand=True)

        # Initials for avatar
        parts = contact["name"].split()
        initials = ""
        if len(parts) >= 2:
            initials = parts[0][0] + parts[1][0]
        elif len(parts) == 1 and parts[0]:
            initials = parts[0][:2]
        else:
            initials = "?"
        
        self.avatar.draw_avatar(initials)
        self.details_name_lbl.config(text=contact["name"])
        self.details_phone_lbl.config(text=contact["phone"])
        self.details_email_lbl.config(text=contact["email"] if contact["email"] else "Not set")
        self.details_address_lbl.config(text=contact["address"] if contact["address"] else "Not set")

    def open_add_dialog(self):
        dialog = ContactDialog(self.parent, title="➕ Add New Contact")
        self.parent.wait_window(dialog)

        if dialog.result:
            new_id = self.db.add_contact(
                name=dialog.result["name"],
                phone=dialog.result["phone"],
                email=dialog.result["email"],
                address=dialog.result["address"]
            )
            self.refresh_contact_list()
            # Select new contact automatically
            self.auto_select_contact(new_id)

    def open_edit_dialog(self):
        if not self.selected_contact_id:
            return
        
        contact = self.db.get_contact(self.selected_contact_id)
        if not contact:
            return

        dialog = ContactDialog(self.parent, title="✏️ Edit Contact", contact=contact)
        self.parent.wait_window(dialog)

        if dialog.result:
            self.db.update_contact(
                contact_id=self.selected_contact_id,
                name=dialog.result["name"],
                phone=dialog.result["phone"],
                email=dialog.result["email"],
                address=dialog.result["address"]
            )
            self.refresh_contact_list()
            
            # Reload detail pane
            updated = self.db.get_contact(self.selected_contact_id)
            self.load_detailed_contact(updated)

    def delete_current_contact(self):
        if not self.selected_contact_id:
            return
        
        contact = self.db.get_contact(self.selected_contact_id)
        if not contact:
            return

        confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete contact '{contact['name']}'?")
        if confirm:
            self.db.delete_contact(self.selected_contact_id)
            self.selected_contact_id = None
            
            # Reset Displays
            self.details_card.pack_forget()
            self.placeholder_lbl.pack(fill="both", expand=True)
            
            self.refresh_contact_list()

    def auto_select_contact(self, contact_id):
        """Utility to select a contact in listbox and display details."""
        for i, c in enumerate(self.contacts_list_data):
            if c["id"] == contact_id:
                self.listbox.selection_clear(0, tk.END)
                self.listbox.selection_set(i)
                self.listbox.activate(i)
                self.selected_contact_id = contact_id
                self.load_detailed_contact(c)
                break

if __name__ == "__main__":
    root = tk.Tk()
    app = GUIContacts(root)
    app.pack(fill="both", expand=True)
    root.mainloop()
