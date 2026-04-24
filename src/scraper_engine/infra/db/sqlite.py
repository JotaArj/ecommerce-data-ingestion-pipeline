from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from time import time

from scraper_engine.core.settings import Settings

SCHEMA_PATH = Path(__file__).with_name("schema.sql")


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
        self._ensure_schema(connection)
        return connection

    def _ensure_schema(self, connection: sqlite3.Connection) -> None:
        self._migrate_legacy_product_tables(connection)
        schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")
        connection.executescript(schema_sql)
        connection.commit()

    def _migrate_legacy_product_tables(
        self, connection: sqlite3.Connection
    ) -> None:
        if not self._has_legacy_product_schema(connection):
            return

        suffix = int(time())
        product_tables = (
            "product_snapshots",
            "product_categories",
            "source_products",
            "products",
        )

        connection.execute("PRAGMA foreign_keys = OFF;")
        for table_name in product_tables:
            if self._table_exists(connection, table_name):
                connection.execute(
                    f"ALTER TABLE {table_name} RENAME TO {table_name}_legacy_{suffix}"
                )
        connection.execute("PRAGMA foreign_keys = ON;")

    def _has_legacy_product_schema(self, connection: sqlite3.Connection) -> bool:
        if self._table_exists(connection, "source_products"):
            return True

        if (
            self._table_exists(connection, "product_categories")
            and "parent_category_id"
            in self._table_columns(connection, "product_categories")
        ):
            return True

        return (
            self._table_exists(connection, "products")
            and (
                "source_site" not in self._table_columns(connection, "products")
                or "type" in self._table_columns(connection, "products")
            )
        )

    def _table_exists(self, connection: sqlite3.Connection, table_name: str) -> bool:
        row = connection.execute(
            """
            SELECT 1
            FROM sqlite_master
            WHERE type = 'table'
              AND name = ?
            """,
            (table_name,),
        ).fetchone()
        return row is not None

    def _table_columns(
        self, connection: sqlite3.Connection, table_name: str
    ) -> set[str]:
        rows = connection.execute(f"PRAGMA table_info({table_name})").fetchall()
        return {str(row["name"]) for row in rows}

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

        connection = sqlite3.connect(self._db_path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON;")
        try:
            self._migrate_legacy_product_tables(connection)
            connection.executescript(schema_sql)
            connection.commit()
        finally:
            connection.close()


def build_database(settings: Settings) -> SQLiteDatabase:
    """
    Factory helper to build the database manager from application settings.
    """
    return SQLiteDatabase(db_path=settings.db_path)
