from __future__ import annotations

import sqlite3
from datetime import datetime
from decimal import Decimal
from pathlib import Path

from scraper_engine.domain.enums import (
    Currency,
    RunStatus,
    RunType,
    SourceSite,
    StockStatus,
)
from scraper_engine.domain.models import Product, ProductSnapshot, ScraperRun
from scraper_engine.infra.db.repositories import (
    ProductRepository,
    ProductSnapshotRepository,
    RunRepository,
)


def test_snapshot_insert_creates_time_series_rows() -> None:
    connection = sqlite3.connect(":memory:")
    connection.executescript(
        Path("src/scraper_engine/infra/db/schema.sql").read_text(encoding="utf-8")
    )
    try:
        run_repository = RunRepository(connection)
        product_repository = ProductRepository(connection)
        snapshot_repository = ProductSnapshotRepository(connection)

        product = Product(
            id="product-1",
            source_site=SourceSite.OXYLABS_SANDBOX,
            source_product_code="1",
            name="Product 1",
            product_type=None,
            rating=None,
            pdp_url="https://example.test/product-1",
            developer=None,
            created_at=datetime(2026, 4, 24, 10, 0, 0),
            updated_at=datetime(2026, 4, 24, 10, 0, 0),
            genre=None,
            description=None,
        )
        product_repository.upsert(product)

        for index, price in enumerate((Decimal("10.00"), Decimal("11.00")), start=1):
            run_id = f"run-{index}"
            run_repository.upsert(
                ScraperRun(
                    id=run_id,
                    run_type=RunType.CATALOG,
                    source_site=SourceSite.OXYLABS_SANDBOX,
                    status=RunStatus.SUCCEEDED,
                    started_at=datetime(2026, 4, 24, 10, index, 0),
                )
            )
            snapshot_repository.insert(
                ProductSnapshot(
                    source_product_id=product.id,
                    run_id=run_id,
                    observed_at=datetime(2026, 4, 24, 10, index, 0),
                    current_price=price,
                    original_price=price,
                    currency=Currency.EUR,
                    stock_status=StockStatus.IN_STOCK,
                    created_at=datetime(2026, 4, 24, 10, index, 0),
                )
            )

        rows = connection.execute(
            """
            SELECT run_id, current_price
            FROM product_snapshots
            WHERE source_product_id = ?
            ORDER BY observed_at
            """,
            (product.id,),
        ).fetchall()

        assert rows == [("run-1", 10), ("run-2", 11)]
    finally:
        connection.close()
