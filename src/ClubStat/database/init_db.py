from pathlib import Path
from .connection import get_connection

SCHEMA_PATH = Path(__file__).with_name("schema.sql")

def init_db() -> None:
    """Create tables and reference data without deleting existing records."""
    with get_connection() as connection:
        connection.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))

if __name__ == "__main__":
    init_db()
    print("База данных ClubStat готова.")
