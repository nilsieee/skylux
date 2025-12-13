import sqlite3
from pathlib import Path


SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS domes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  code TEXT NOT NULL UNIQUE,
  location TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS interventions (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  dome_id INTEGER NOT NULL,
  date TEXT NOT NULL,
  kind TEXT NOT NULL,
  note TEXT,
  FOREIGN KEY (dome_id) REFERENCES domes(id)
);
"""


def get_connection(db_path: str) -> sqlite3.Connection:
    """Create a sqlite connection and enforce foreign keys."""
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def init_db(db_path: str) -> None:
    """Ensure the database file + schema exist."""
    # Make sure parent folder exists (e.g. db/)
    Path(db_path).parent.mkdir(parents=True, exist_ok=True)

    with get_connection(db_path) as conn:
        conn.executescript(SCHEMA_SQL)
