from __future__ import annotations

from enum import StrEnum


class SourceSite(StrEnum):

    OXYLABS_SANDBOX = "oxylabs_sandbox"
    WEBSCRAPER_ECOMMERCE_AJAX = "webscraper_ecommerce_ajax"


class RunType(StrEnum):

    CATALOG = "catalog"
    ENRICHMENT = "enrichment"
    SNAPSHOT = "snapshot"


class RunStatus(StrEnum):

    PENDING = "pending"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


class Currency(StrEnum):

    EUR = "EUR"
    USD = "USD"
    UNKNOWN = "UNKNOWN"


class StockStatus(StrEnum):

    IN_STOCK = "in_stock"
    OUT_OF_STOCK = "out_of_stock"
    UNKNOWN = "unknown"
