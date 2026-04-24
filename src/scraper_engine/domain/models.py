from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from scraper_engine.domain.enums import (
    Currency,
    RunStatus,
    RunType,
    SourceSite,
    StockStatus,
)


@dataclass(slots=True)
class Product:
    id: str
    source_site: SourceSite
    source_product_code: str
    name: str
    type: str | None
    rating: str | None
    pdp_url: str
    developer: str | None
    created_at: datetime
    updated_at: datetime
    genre: list[str] | None
    description: str | None = None


@dataclass(slots=True)
class CategoryNode:
    id: str
    source_site: SourceSite
    source_category_code: str
    name: str
    url: str
    path: str
    parent_id: str | None
    level: int
    is_leaf: bool
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class ProductCategoryLink:
    source_product_id: str 
    category_id: str
    created_at: datetime


@dataclass(slots=True)
class ProductSnapshot:
    source_product_id: str
    run_id: str
    observed_at: datetime
    current_price: Decimal | None
    original_price: Decimal | None # como encontrar?
    currency: Currency #capturar con el texto
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