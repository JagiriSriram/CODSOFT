import sqlite3
import os
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_name="todo_tasks.db"):
        # Put the database in the same directory as this script
        script_dir = os.path.dirname(os.path.abspath(__file__))
        self.db_path = os.path.join(script_dir, db_name)
        self.init_db()

    def _get_connection(self):
        """Returns a connection to the SQLite database."""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row  # Access columns by name
        return conn

    def init_db(self):
        """Creates the tasks table if it does not exist."""
        query = """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            priority TEXT DEFAULT 'Medium',
            category TEXT DEFAULT 'General',
            due_date TEXT,
            status TEXT DEFAULT 'Pending',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
        """
        with self._get_connection() as conn:
            conn.execute(query)
            conn.commit()

    def add_task(self, title, description, priority="Medium", category="General", due_date=""):
        """Inserts a new task into the database."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        INSERT INTO tasks (title, description, priority, category, due_date, status, created_at, updated_at)
        VALUES (?, ?, ?, ?, ?, 'Pending', ?, ?)
        """
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (title, description, priority, category, due_date, now, now))
            conn.commit()
            return cursor.lastrowid

    def update_task(self, task_id, title, description, priority, category, due_date, status):
        """Updates an existing task in the database."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        UPDATE tasks
        SET title = ?, description = ?, priority = ?, category = ?, due_date = ?, status = ?, updated_at = ?
        WHERE id = ?
        """
        with self._get_connection() as conn:
            conn.execute(query, (title, description, priority, category, due_date, status, now, task_id))
            conn.commit()

    def update_status(self, task_id, status):
        """Quickly toggle or set the status of a task (Pending/Completed)."""
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        query = """
        UPDATE tasks
        SET status = ?, updated_at = ?
        WHERE id = ?
        """
        with self._get_connection() as conn:
            conn.execute(query, (status, now, task_id))
            conn.commit()

    def delete_task(self, task_id):
        """Deletes a task from the database by its ID."""
        query = "DELETE FROM tasks WHERE id = ?"
        with self._get_connection() as conn:
            conn.execute(query, (task_id,))
            conn.commit()

    def get_task(self, task_id):
        """Fetches a single task by ID."""
        query = "SELECT * FROM tasks WHERE id = ?"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None

    def get_tasks(self, search_query=None, status_filter=None, priority_filter=None, category_filter=None, sort_by=None):
        """
        Fetches tasks matching the criteria, with optional sorting.
        
        sort_by options: 'due_date_asc', 'due_date_desc', 'priority_high_first', 'created_at_desc'
        """
        query = "SELECT * FROM tasks WHERE 1=1"
        params = []

        if search_query:
            query += " AND (title LIKE ? OR description LIKE ?)"
            like_pat = f"%{search_query}%"
            params.extend([like_pat, like_pat])

        if status_filter and status_filter != "All":
            query += " AND status = ?"
            params.append(status_filter)

        if priority_filter and priority_filter != "All":
            query += " AND priority = ?"
            params.append(priority_filter)

        if category_filter and category_filter != "All":
            query += " AND category = ?"
            params.append(category_filter)

        # Ordering
        if sort_by == 'due_date_asc':
            # Handle empty/null due dates so they appear at the bottom
            query += " ORDER BY CASE WHEN due_date IS NULL OR due_date = '' THEN 1 ELSE 0 END, due_date ASC"
        elif sort_by == 'due_date_desc':
            query += " ORDER BY CASE WHEN due_date IS NULL OR due_date = '' THEN 1 ELSE 0 END, due_date DESC"
        elif sort_by == 'priority_high_first':
            query += """ ORDER BY 
                CASE priority 
                    WHEN 'High' THEN 1 
                    WHEN 'Medium' THEN 2 
                    WHEN 'Low' THEN 3 
                    ELSE 4 
                END ASC, created_at DESC"""
        else:  # Default: created_at_desc
            query += " ORDER BY created_at DESC"

        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

    def get_categories(self):
        """Returns all distinct categories present in the tasks table."""
        query = "SELECT DISTINCT category FROM tasks WHERE category IS NOT NULL AND category != ''"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query)
            rows = cursor.fetchall()
            # Include default categories in case they aren't in the database yet
            defaults = {"General", "Work", "Personal", "Shopping", "Health"}
            db_cats = {row['category'] for row in rows}
            return sorted(list(defaults.union(db_cats)))
