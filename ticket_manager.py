# Import sqlite3 so Python can create and talk to our local database file
import sqlite3

# Import datetime so we can stamp the exact date and time on every ticket
from datetime import datetime

# Name of our database file on the computer
DB_NAME = "helpdesk.db"


def init_db():
    # Connect to the database file (if it does not exist, Python creates it)
    with sqlite3.connect(DB_NAME) as conn:
        # The cursor is like a pen used to write and execute SQL commands
        cursor = conn.cursor()

        # Create a table called 'tickets' if we haven't already made one
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT, -- Auto gives each ticket a unique number (1, 2, 3...)
                title TEXT NOT NULL,                  -- What the problem is
                category TEXT NOT NULL,               -- Type of issue (e.g., Network, Hardware)
                priority TEXT NOT NULL,               -- How urgent it is (e.g., Low, High)
                status TEXT DEFAULT 'Open',           -- Current state (starts as 'Open')
                source TEXT DEFAULT 'Manual',         -- Where it came from (User or Log Monitor)
                created_at TEXT NOT NULL              -- When it was created
            )
        """
        )

        # Save the changes to the database file
        conn.commit()


def create_ticket(title, category, priority, source="Manual"):
    # Connect to the database
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Get the current date and time formatted nicely (Year-Month-Day Hour:Minute:Second)
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Insert the new ticket information into the table
        cursor.execute(
            """
            INSERT INTO tickets (title, category, priority, status, source, created_at)
            VALUES (?, ?, ?, 'Open', ?, ?)
        """,
            (title, category, priority, source, now),
        )

        # Save the changes
        conn.commit()

        # Return the new ticket's ID number so we know what was just created
        return cursor.lastrowid


def get_all_tickets():
    # Connect to the database
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Ask the database to give us all ticket records, newest first (ORDER BY id DESC)
        cursor.execute(
            "SELECT id, title, category, priority, status, source, created_at FROM tickets ORDER BY id DESC"
        )

        # Grab all the results and return them as a list
        return cursor.fetchall()


def update_status(ticket_id, new_status):
    # Connect to the database
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()

        # Find the ticket by its ID and change its status column
        cursor.execute(
            "UPDATE tickets SET status = ? WHERE id = ?",
            (new_status, ticket_id),
        )

        # Save the update
        conn.commit()


# This block only runs if you run this file directly in the terminal: python ticket_manager.py
if __name__ == "__main__":
    init_db()
    print("Database initialized successfully.")