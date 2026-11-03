
import sqlite3

from contextlib import contextmanager
from pathlib import Path


# Project root
BASE_DIR = Path(__file__).resolve().parent.parent

# Database location
DB_PATH = BASE_DIR / "data" / "biai_crm.db"

# SQL schema location
SCHEMA_PATH = BASE_DIR / "database" / "schema.sql"


@contextmanager
def get_connection():
    """
    Provide a safe SQLite database connection.
    """

    DB_PATH.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    connection = sqlite3.connect(
        DB_PATH,
        timeout=10
    )

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


def initialize_database():
    """
    Create database tables and indexes.
    """

    if not SCHEMA_PATH.exists():
        raise FileNotFoundError(
            f"Schema file not found: {SCHEMA_PATH}"
        )

    schema = SCHEMA_PATH.read_text(
        encoding="utf-8"
    )

    with get_connection() as connection:
        connection.executescript(schema)

    print("Database initialized successfully!")
    print(f"Database location: {DB_PATH}")
