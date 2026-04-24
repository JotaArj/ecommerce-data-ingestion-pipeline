from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager
import sqlite3
from pathlib import Path

from scraper_engine.core.settings import Settings


class SQLiteDatabase:
    """
    Lightweight SQLite database manager.

    Responsibilities:
    - open connections
    - enforce foreign keys
    - initialize schema
    """

    def __init__(self, db_path: Path) -> None:
        self._db_path = db_path

    @property
    def db_path(self) -> Path:
        return self._db_path

    def connect(self) -> sqlite3.Connection:
        """
        Create a new SQLite connection with row access by column name.
        """
        self._db_path.parent.mkdir(parents=True, exist_ok=True)

        connection = sqlite3.connect(self._db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        return connection

    @contextmanager
    def session(self) -> Iterator[sqlite3.Connection]:
        connection = self.connect()
        try:
            yield connection
            connection.commit()
        except Exception:
            connection.rollback()
            raise
        finally:
            connection.close()

    def initialize(self, schema_path: Path) -> None:
        """
        Create database objects from the schema.sql file.
        """
        schema_sql = schema_path.read_text(encoding="utf-8")

        with self.connect() as connection:
            connection.executescript(schema_sql)
            connection.commit()


def build_database(settings: Settings) -> SQLiteDatabase:
    """
    Factory helper to build the database manager from application settings.
    """
    return SQLiteDatabase(db_path=settings.db_path)
