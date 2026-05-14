from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from ecommerce_ingestion.domain.enums import (
    Currency,
    RunStatus,
    RunType,
    SourceSite,
    StockStatus,
)


@dataclass(slots=True)
class GameProduct:
    game_id: str
    game_source_site: SourceSite
    source_game_product_code: str
    game_name: str
    game_product_type: str | None
    game_rating: str | None
    game_pdp_url: str
    game_developer: str | None
    game_created_at: datetime
    game_updated_at: datetime
    game_description: str | None = None


@dataclass(slots=True)
class CategoryNode:
    category_id: str
    category_source_site: SourceSite
    source_category_code: str
    category_name: str
    category_url: str
    category_path: str
    category_parent_id: str | None
    category_level: int
    category_is_leaf: bool
    category_created_at: datetime
    category_updated_at: datetime


@dataclass(slots=True)
class GameProductCategoryLink:
    game_product_id: str
    category_id: str
    created_at: datetime


@dataclass(slots=True)
class GameProductSnapshot:
    game_product_id: str
    run_id: str
    observed_at: datetime
    current_price: Decimal | None
    original_price: Decimal | None
    currency: Currency
    stock_status: StockStatus
    meta_score: Decimal | None = None
    user_score: Decimal | None = None
    created_at: datetime | None = None


@dataclass(slots=True)
class ScraperRun:
    id: str
    run_type: RunType
    source_site: SourceSite
    status: RunStatus
    started_at: datetime
    finished_at: datetime | None = None
    error_message: str | None = None

@dataclass(slots=True)
class GameGenre:
    genre_id: str

@dataclass(slots=True)
class GameGenreLink:
    game_id: str
    genre_id: str
