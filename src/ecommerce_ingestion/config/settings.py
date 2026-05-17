import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from ecommerce_ingestion.config.constants import (
    BRONZE_DIR,
    DEFAULT_BASE_URL,
    DEFAULT_HEADLESS,
    DEFAULT_LOG_LEVEL,
    DEFAULT_SCRAPING_URL,
    LOGS_DIR,
)
from ecommerce_ingestion.domain.enums import SourceSite

load_dotenv()


def _get_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


def _get_path(value: str | None, default: Path) -> Path:
    if value:
        return Path(value)
    return default


def _default_log_file_path(source_name: str) -> Path:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return LOGS_DIR / f"{source_name}_scraper_{timestamp}.log"


@dataclass(slots=True)
class Settings:
    source_site: SourceSite
    base_url: str
    start_scraping_url: str
    headless: bool
    db_path: Path
    log_level: str
    log_file_path: Path


def load_scrapper_settings(source_site: SourceSite) -> Settings:
    source_site = SourceSite(
        os.getenv("SOURCE_SITE", SourceSite.OXYLABS_SANDBOX.value)
    )
    source_name = source_site.value

    return Settings(
        source_site=source_site,
        base_url=os.getenv("BASE_URL", DEFAULT_BASE_URL),
        start_scraping_url=os.getenv("START_SCRAPING_URL", DEFAULT_SCRAPING_URL),
        headless=_get_bool(os.getenv("HEADLESS"), DEFAULT_HEADLESS),
        db_path=_get_path(
            os.getenv("DB_PATH"),
            BRONZE_DIR / f"{source_name}_scraper.db",
        ),
        log_level=os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL),
        log_file_path=_get_path(
            os.getenv("LOG_FILE_PATH"),
            _default_log_file_path(source_name),
        )
    )

def load_silver_settings() -> Settings:
    source_site = SourceSite(
        os.getenv("SOURCE_SITE", SourceSite.SILVER_DATA_PROCESSING.value)
    )
    return Settings(
        source_site = source_site,
        base_url="",
        start_scraping_url="",
        headless=False,
        db_path = Path(""),
        log_level=os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL),
        log_file_path=_get_path(
            os.getenv("LOG_FILE_PATH"),
            LOGS_DIR / 
            f"silver_data_processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
        ),
    )

def load_gold_settings() -> Settings:
    source_site = SourceSite(
        os.getenv("SOURCE_SITE", SourceSite.GOLD_DATA_PROCESSING.value)
    )
    return Settings(
        source_site = source_site,
        base_url="",
        start_scraping_url="",
        headless=False,
        db_path = Path(""),
        log_level=os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL),
        log_file_path=_get_path(
            os.getenv("LOG_FILE_PATH"),
            LOGS_DIR / 
            f"gold_data_processing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log",
        ),
    )
