from __future__ import annotations

from enum import Enum


class SourceSite(str, Enum):

    OXYLABS_SANDBOX = "oxylabs_sandbox"
    WEBSCRAPER_ECOMMERCE_AJAX = "webscraper_ecommerce_ajax"


class RunType(str, Enum):

    CATALOG = "catalog"
    ENRICHMENT = "enrichment"
    SNAPSHOT = "snapshot"


class RunStatus(str, Enum):

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class Currency(str, Enum):

    EUR = "EUR"
    USD = "USD"
    UNKNOWN = "UNKNOWN"


class StockStatus(str, Enum):

    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    UNKNOWN = "unknown"
