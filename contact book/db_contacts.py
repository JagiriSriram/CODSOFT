import sqlite3
import os
from datetime import datetime

class ContactDatabase:
    def __init__(self, db_name="contacts.db"):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(script_dir, db_name)
        self.init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self):
        """Creates the contacts table if it does not exist."""
        query = """
        CREATE TABLE IF NOT EXISTS contacts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            email TEXT,
            address TEXT,
            created_at TEXT NOT NULL
        )
        """
        with self._get_connection() as conn:
            conn.execute(query)
            conn.commit()

    def add_contact(self, name, phone, email="", address=""):
        """Inserts a new contact. Returns the newly created contact ID."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO contacts (name, phone, email, address, created_at)
        VALUES (?, ?, ?, ?, ?)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (name, phone, email, address, now))
            conn.commit()
            return cursor.lastrowid

    def get_contact(self, contact_id):
        """Fetches a single contact by its ID."""
        query = "SELECT * FROM contacts WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (contact_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_contacts(self, search_query=None):
        """
        Fetches contacts from the database. 
        If search_query is provided, searches by name or phone number.
        """
        query = "SELECT * FROM contacts"
        params = []

        if search_query:
            query += " WHERE name LIKE ? OR phone LIKE ?"
            like_pat = f"%{search_query}%"
            params.extend([like_pat, like_pat])

        query += " ORDER BY name COLLATE NOCASE ASC"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def update_contact(self, contact_id, name, phone, email="", address=""):
        """Updates an existing contact's details."""
        query = """
        UPDATE contacts
        SET name = ?, phone = ?, email = ?, address = ?
        WHERE id = ?
        """
        with self._get_connection() as conn:
            conn.execute(query, (name, phone, email, address, contact_id))
            conn.commit()

    def delete_contact(self, contact_id):
        """Deletes a contact by ID."""
        query = "DELETE FROM contacts WHERE id = ?"
        with self._get_connection() as conn:
            conn.execute(query, (contact_id,))
            conn.commit()
