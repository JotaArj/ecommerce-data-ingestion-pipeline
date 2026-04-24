from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from scraper_engine.core.constants import (
    DEFAULT_BASE_URL,
    DEFAULT_DB_PATH,
    DEFAULT_HEADLESS,
    DEFAULT_LOG_FILE_PATH,
    DEFAULT_LOG_LEVEL,
    DEFAULT_SCRAP_URL,
)
from scraper_engine.domain.enums import SourceSite

load_dotenv()


def _get_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


@dataclass(slots=True)
class Settings:
    # --- scraper ---
    source_site: SourceSite
    base_url: str
    start_scraping_url: str

    # --- browser ---
    headless: bool

    # --- infra ---
    db_path: Path
    log_level: str
    log_file_path: Path


def load_settings() -> Settings:
    return Settings(
        source_site=SourceSite(
            os.getenv("SOURCE_SITE", SourceSite.OXYLABS_SANDBOX.value)
        ),
        base_url=os.getenv("BASE_URL", DEFAULT_BASE_URL),
        start_scraping_url=os.getenv("START_SCRAPING_URL", DEFAULT_SCRAP_URL),
        headless=_get_bool(os.getenv("HEADLESS"), DEFAULT_HEADLESS),
        db_path=Path(os.getenv("DB_PATH", str(DEFAULT_DB_PATH))),
        log_level=os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL),
        log_file_path=Path(os.getenv("LOG_FILE_PATH", str(DEFAULT_LOG_FILE_PATH))),
    )