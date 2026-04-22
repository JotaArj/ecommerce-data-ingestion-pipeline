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
    canonical_code: str | None
    canonical_name: str | None
    brand: str | None
    created_at: datetime
    updated_at: datetime


@dataclass(slots=True)
class SourceProduct:
    id: str
    product_id: str | None
    source_site: SourceSite
    source_product_code: str
    name: str
    pdp_url: str
    brand: str | None
    created_at: datetime
    updated_at: datetime


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
    is_primary: bool
    created_at: datetime


@dataclass(slots=True)
class ProductSnapshot:
    source_product_id: str
    run_id: str
    observed_at: datetime
    current_price: Decimal | None
    original_price: Decimal | None
    currency: Currency
    stock_status: StockStatus
    rating: Decimal | None = None
    review_count: int | None = None
    image_url: str | None = None
    description: str | None = None
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