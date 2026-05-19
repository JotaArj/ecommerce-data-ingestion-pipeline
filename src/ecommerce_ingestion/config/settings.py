import os
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from ecommerce_ingestion.config.paths import BRONZE_DIR, LOGS_DIR
from ecommerce_ingestion.config.source_config import (
    DEFAULT_BASE_URL,
    DEFAULT_HEADLESS,
    DEFAULT_LOG_LEVEL,
    DEFAULT_SCRAPING_URL,
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


def default_run_name() -> str:
    return f"pipeline_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"


def _default_log_file_path(log_name: str, run_name: str | None = None) -> Path:
    run_dir_name = run_name or default_run_name()
    return LOGS_DIR / run_dir_name / f"{log_name}.log"


@dataclass(slots=True)
class LogSettings:
    log_level: str
    log_file_path: Path


@dataclass(slots=True)
class ScraperSettings(LogSettings):
    source_site: SourceSite
    base_url: str
    start_scraping_url: str
    headless: bool
    db_path: Path


def load_scrapper_settings(
    source_site: SourceSite,
    run_name: str | None = None,
) -> ScraperSettings:
    source_site = SourceSite(
        os.getenv("SOURCE_SITE", SourceSite.OXYLABS_SANDBOX.value)
    )
    source_name = source_site.value

    return ScraperSettings(
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
            _default_log_file_path(f"{source_name}_scraper", run_name),
        )
    )

def load_log_settings(type_name: str, run_name: str | None = None) -> LogSettings:
    return LogSettings(
        log_level=os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL),
        log_file_path=_get_path(
            os.getenv("LOG_FILE_PATH"),
            _default_log_file_path(f"{type_name}_data_processing", run_name),
        ),
    )
