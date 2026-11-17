import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "clubstat.db"

@contextmanager
def get_connection() -> Iterator[sqlite3.Connection]:
    """Open a SQLite connection with foreign keys enabled and always close it."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
