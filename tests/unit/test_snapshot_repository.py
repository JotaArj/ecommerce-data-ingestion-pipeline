from __future__ import annotations

import sqlite3
from datetime import datetime
from decimal import Decimal
from importlib import resources

from ecommerce_ingestion.db.repositories import (
    GameGenreGameLinkRepository,
    GameGenreRepository,
    GameProductRepository,
    GameProductSnapshotRepository,
    RunRepository,
)
from ecommerce_ingestion.domain.enums import (
    Currency,
    RunStatus,
    RunType,
    SourceSite,
    StockStatus,
)
from ecommerce_ingestion.domain.models import (
    GameGenre,
    GameGenreLink,
    GameProduct,
    GameProductSnapshot,
    ScraperRun,
)


def test_snapshot_insert_creates_time_series_rows() -> None:
    connection = sqlite3.connect(":memory:")
    schema_sql = resources.files("ecommerce_ingestion.db").joinpath(
        "schema.sql"
    ).read_text(encoding="utf-8")
    connection.executescript(schema_sql)
    try:
        run_repository = RunRepository(connection)
        game_product_repository = GameProductRepository(connection)
        game_product_snapshot_repository = GameProductSnapshotRepository(connection)

        game_product = GameProduct(
            game_id="product-1",
            game_source_site=SourceSite.OXYLABS_SANDBOX,
            source_game_product_code="1",
            game_name="Product 1",
            game_product_type=None,
            game_rating=None,
            game_pdp_url="https://example.test/product-1",
            game_developer=None,
            game_created_at=datetime(2026, 4, 24, 10, 0, 0),
            game_updated_at=datetime(2026, 4, 24, 10, 0, 0),
            game_description=None,
        )
        game_product_repository.upsert(game_product)

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
            game_product_snapshot_repository.insert(
                GameProductSnapshot(
                    game_product_id=game_product.game_id,
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
            FROM game_product_snapshots
            WHERE game_product_id = ?
            ORDER BY observed_at
            """,
            (game_product.game_id,),
        ).fetchall()

        assert rows == [("run-1", 10), ("run-2", 11)]
    finally:
        connection.close()


def test_genre_link_insert_requires_existing_game_and_genre() -> None:
    connection = sqlite3.connect(":memory:")
    schema_sql = resources.files("ecommerce_ingestion.db").joinpath(
        "schema.sql"
    ).read_text(encoding="utf-8")
    connection.executescript(schema_sql)
    try:
        game_product_repository = GameProductRepository(connection)
        game_genre_repository = GameGenreRepository(connection)
        game_genre_link_repository = GameGenreGameLinkRepository(connection)

        game_product_repository.upsert(
            GameProduct(
                game_id="product-1",
                game_source_site=SourceSite.OXYLABS_SANDBOX,
                source_game_product_code="1",
                game_name="Product 1",
                game_product_type=None,
                game_rating=None,
                game_pdp_url="https://example.test/product-1",
                game_developer=None,
                game_created_at=datetime(2026, 4, 24, 10, 0, 0),
                game_updated_at=datetime(2026, 4, 24, 10, 0, 0),
                game_description=None,
            )
        )
        game_genre_repository.upsert(GameGenre(genre_id="action adventure"))

        game_genre_link_repository.upsert(
            GameGenreLink(game_id="product-1", genre_id="action adventure")
        )

        rows = connection.execute(
            """
            SELECT game_id, genre_id
            FROM game_genre_game_link
            """
        ).fetchall()

        assert rows == [("product-1", "action adventure")]
    finally:
        connection.close()
