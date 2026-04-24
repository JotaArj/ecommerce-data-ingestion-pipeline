from __future__ import annotations

import json
import sqlite3
from datetime import datetime
from decimal import Decimal

from scraper_engine.domain.models import (
    CategoryNode,
    Product,
    ProductCategoryLink,
    ProductSnapshot,
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


class ProductRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def upsert(self, product: Product) -> None:
        self._connection.execute(
            """
            INSERT INTO products (
                id,
                source_site,
                source_product_code,
                name,
                product_type,
                rating,
                pdp_url,
                developer,
                created_at,
                updated_at,
                genre,
                description
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                source_site = excluded.source_site,
                source_product_code = excluded.source_product_code,
                name = excluded.name,
                product_type = excluded.product_type,
                rating = excluded.rating,
                pdp_url = excluded.pdp_url,
                developer = excluded.developer,
                updated_at = excluded.updated_at,
                genre = excluded.genre,
                description = excluded.description
            """,
            (
                product.id,
                product.source_site.value,
                product.source_product_code,
                product.name,
                product.product_type,
                product.rating,
                product.pdp_url,
                product.developer,
                _dt(product.created_at),
                _dt(product.updated_at),
                json.dumps(product.genre) if product.genre is not None else None,
                product.description,
            ),
        )


class CategoryRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def upsert(self, category: CategoryNode) -> None:
        self._connection.execute(
            """
            INSERT INTO categories (
                id,
                source_site,
                source_category_code,
                name,
                url,
                path,
                parent_id,
                level,
                is_leaf,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                source_site = excluded.source_site,
                source_category_code = excluded.source_category_code,
                name = excluded.name,
                url = excluded.url,
                path = excluded.path,
                parent_id = excluded.parent_id,
                level = excluded.level,
                is_leaf = excluded.is_leaf,
                updated_at = excluded.updated_at
            """,
            (
                category.id,
                category.source_site.value,
                category.source_category_code,
                category.name,
                category.url,
                category.path,
                category.parent_id,
                category.level,
                _bool_to_int(category.is_leaf),
                _dt(category.created_at),
                _dt(category.updated_at),
            ),
        )


class ProductCategoryRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def upsert(self, link: ProductCategoryLink) -> None:
        self._connection.execute(
            """
            INSERT INTO product_categories (
                source_product_id,
                category_id,
                created_at
            )
            VALUES (?, ?, ?)
            ON CONFLICT(source_product_id, category_id) DO NOTHING
            """,
            (
                link.source_product_id,
                link.category_id,
                _dt(link.created_at),
            ),
        )


class ProductSnapshotRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def insert(self, snapshot: ProductSnapshot) -> None:
        created_at = snapshot.created_at or datetime.utcnow()

        self._connection.execute(
            """
            INSERT INTO product_snapshots (
                source_product_id,
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
                snapshot.source_product_id,
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
