import sqlite3
import os
from datetime import datetime

# =====================================================
# Create Database Folder
# =====================================================

os.makedirs("database", exist_ok=True)

# =====================================================
# Connect Database
# =====================================================

conn = sqlite3.connect(
    "database/users.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =====================================================
# USERS TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL
)
""")

# =====================================================
# HISTORY TABLE
# =====================================================

cursor.execute("""
CREATE TABLE IF NOT EXISTS history(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    age INTEGER,
    prediction TEXT,
    probability REAL,
    date TEXT
)
""")

conn.commit()

# =====================================================
# USER FUNCTIONS
# =====================================================

def add_user(username, email, password):
    cursor.execute(
        """
        INSERT INTO users(username,email,password)
        VALUES(?,?,?)
        """,
        (username, email, password)
    )
    conn.commit()


def get_user(username):
    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE username=?
        """,
        (username,)
    )
    return cursor.fetchone()

# =====================================================
# HISTORY FUNCTIONS
# =====================================================

def save_prediction(username, age, prediction, probability):
    """
    Saves prediction history.
    Date is generated automatically.
    """

    current_date = datetime.now().strftime("%d-%m-%Y %H:%M")

    cursor.execute(
        """
        INSERT INTO history
        (username, age, prediction, probability, date)
        VALUES(?,?,?,?,?)
        """,
        (
            username,
            age,
            prediction,
            probability,
            current_date
        )
    )

    conn.commit()


def get_history(username):

    cursor.execute(
        """
        SELECT
            age,
            prediction,
            probability,
            date
        FROM history
        WHERE username=?
        ORDER BY id DESC
        """,
        (username,)
    )

    return cursor.fetchall()


def delete_history():

    cursor.execute("DELETE FROM history")

    conn.commit()