import json
import sqlite3
from datetime import datetime
from decimal import Decimal

from ecommerce_ingestion.domain.models import (
    CategoryNode,
    GameProduct,
    GameProductCategoryLink,
    GameProductSnapshot,
    ScraperRun,
)


def _dt(value: datetime | None) -> str | None:
    return value.isoformat() if value is not None else None


def _bool_to_int(value: bool) -> int:
    return 1 if value else 0


def _decimal_to_str(value: Decimal | None) -> str | None:
    return str(value) if value is not None else None


class RunRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def upsert(self, run: ScraperRun) -> None:
        self._connection.execute(
            """
            INSERT INTO runs (
                id,
                run_type,
                source_site,
                status,
                started_at,
                finished_at,
                error_message
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                run_type = excluded.run_type,
                source_site = excluded.source_site,
                status = excluded.status,
                started_at = excluded.started_at,
                finished_at = excluded.finished_at,
                error_message = excluded.error_message
            """,
            (
                run.id,
                run.run_type.value,
                run.source_site.value,
                run.status.value,
                _dt(run.started_at),
                _dt(run.finished_at),
                run.error_message,
            ),
        )


class GameProductRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def upsert(self, game_product: GameProduct) -> None:
        self._connection.execute(
            """
            INSERT INTO game_products (
                game_id,
                game_source_site,
                source_game_product_code,
                game_name,
                game_product_type,
                game_rating,
                game_pdp_url,
                game_developer,
                game_created_at,
                game_updated_at,
                game_genre,
                game_description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(game_id) DO UPDATE SET
                game_source_site = excluded.game_source_site,
                source_game_product_code = excluded.source_game_product_code,
                game_name = excluded.game_name,
                game_product_type = excluded.game_product_type,
                game_rating = excluded.game_rating,
                game_pdp_url = excluded.game_pdp_url,
                game_developer = excluded.game_developer,
                game_updated_at = excluded.game_updated_at,
                game_genre = excluded.game_genre,
                game_description = excluded.game_description
            """,
            (
                game_product.game_id,
                game_product.game_source_site.value,
                game_product.source_game_product_code,
                game_product.game_name,
                game_product.game_product_type,
                game_product.game_rating,
                game_product.game_pdp_url,
                game_product.game_developer,
                _dt(game_product.game_created_at),
                _dt(game_product.game_updated_at),
                json.dumps(game_product.game_genre)
                if game_product.game_genre is not None
                else None,
                game_product.game_description,
            ),
        )


class CategoryRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def exists(self, category_id: str) -> bool:
        row = self._connection.execute(
            """
            SELECT 1
            FROM category_nodes
            WHERE category_id = ?
            LIMIT 1
            """,
            (category_id,),
        ).fetchone()
        return row is not None

    def upsert(self, category: CategoryNode) -> None:
        self._connection.execute(
            """
            INSERT INTO category_nodes (
                category_id,
                category_source_site,
                source_category_code,
                category_name,
                category_url,
                category_path,
                category_parent_id,
                category_level,
                category_is_leaf,
                category_created_at,
                category_updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(category_id) DO UPDATE SET
                category_source_site = excluded.category_source_site,
                source_category_code = excluded.source_category_code,
                category_name = excluded.category_name,
                category_url = excluded.category_url,
                category_path = excluded.category_path,
                category_parent_id = excluded.category_parent_id,
                category_level = excluded.category_level,
                category_is_leaf = excluded.category_is_leaf,
                category_updated_at = excluded.category_updated_at
            """,
            (
                category.category_id,
                category.category_source_site.value,
                category.source_category_code,
                category.category_name,
                category.category_url,
                category.category_path,
                category.category_parent_id,
                category.category_level,
                _bool_to_int(category.category_is_leaf),
                _dt(category.category_created_at),
                _dt(category.category_updated_at),
            ),
        )


class GameProductCategoryRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def upsert(self, link: GameProductCategoryLink) -> None:
        self._connection.execute(
            """
            INSERT INTO game_product_categories (
                game_product_id,
                category_id,
                created_at
            )
            VALUES (?, ?, ?)
            ON CONFLICT(game_product_id, category_id) DO NOTHING
            """,
            (
                link.game_product_id,
                link.category_id,
                _dt(link.created_at),
            ),
        )


class GameProductSnapshotRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def insert(self, snapshot: GameProductSnapshot) -> None:
        created_at = snapshot.created_at or datetime.utcnow()

        self._connection.execute(
            """
            INSERT INTO game_product_snapshots (
                game_product_id,
                run_id,
                observed_at,
                current_price,
                original_price,
                currency,
                stock_status,
                meta_score,
                user_score,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                snapshot.game_product_id,
                snapshot.run_id,
                _dt(snapshot.observed_at),
                _decimal_to_str(snapshot.current_price),
                _decimal_to_str(snapshot.original_price),
                snapshot.currency.value,
                snapshot.stock_status.value,
                _decimal_to_str(snapshot.meta_score),
                _decimal_to_str(snapshot.user_score),
                _dt(created_at),
            ),
        )
