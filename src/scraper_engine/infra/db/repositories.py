from __future__ import annotations

import sqlite3
from datetime import datetime
from decimal import Decimal

from scraper_engine.domain.models import (
    CategoryNode,
    Product,
    ProductCategoryLink,
    ProductSnapshot,
    ScraperRun,
    SourceProduct,
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
        self._connection.commit()


class ProductRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def upsert(self, product: Product) -> None:
        self._connection.execute(
            """
            INSERT INTO products (
                id,
                canonical_code,
                canonical_name,
                brand,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                canonical_code = excluded.canonical_code,
                canonical_name = excluded.canonical_name,
                brand = excluded.brand,
                updated_at = excluded.updated_at
            """,
            (
                product.id,
                product.canonical_code,
                product.canonical_name,
                product.brand,
                _dt(product.created_at),
                _dt(product.updated_at),
            ),
        )
        self._connection.commit()


class SourceProductRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def upsert(self, source_product: SourceProduct) -> None:
        self._connection.execute(
            """
            INSERT INTO source_products (
                id,
                product_id,
                source_site,
                source_product_code,
                name,
                pdp_url,
                brand,
                created_at,
                updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                product_id = excluded.product_id,
                source_site = excluded.source_site,
                source_product_code = excluded.source_product_code,
                name = excluded.name,
                pdp_url = excluded.pdp_url,
                brand = excluded.brand,
                updated_at = excluded.updated_at
            """,
            (
                source_product.id,
                source_product.product_id,
                source_product.source_site.value,
                source_product.source_product_code,
                source_product.name,
                source_product.pdp_url,
                source_product.brand,
                _dt(source_product.created_at),
                _dt(source_product.updated_at),
            ),
        )
        self._connection.commit()


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
        self._connection.commit()


class ProductCategoryRepository:
    def __init__(self, connection: sqlite3.Connection) -> None:
        self._connection = connection

    def upsert(self, link: ProductCategoryLink) -> None:
        self._connection.execute(
            """
            INSERT INTO product_categories (
                source_product_id,
                category_id,
                is_primary,
                created_at
            )
            VALUES (?, ?, ?, ?)
            ON CONFLICT(source_product_id, category_id) DO UPDATE SET
                is_primary = excluded.is_primary
            """,
            (
                link.source_product_id,
                link.category_id,
                _bool_to_int(link.is_primary),
                _dt(link.created_at),
            ),
        )
        self._connection.commit()


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
                rating,
                review_count,
                image_url,
                description,
                created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                snapshot.source_product_id,
                snapshot.run_id,
                _dt(snapshot.observed_at),
                _decimal_to_str(snapshot.current_price),
                _decimal_to_str(snapshot.original_price),
                snapshot.currency.value,
                snapshot.stock_status.value,
                _decimal_to_str(snapshot.rating),
                snapshot.review_count,
                snapshot.image_url,
                snapshot.description,
                _dt(created_at),
            ),
        )
        self._connection.commit()
