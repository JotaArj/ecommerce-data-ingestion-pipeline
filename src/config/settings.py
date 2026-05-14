import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from src.config.constants import (
    DB_OUTPUT_DIR,
    DEFAULT_BASE_URL,
    DEFAULT_HEADLESS,
    DEFAULT_LOG_LEVEL,
    DEFAULT_SCRAP_URL,
    LOGS_DIR,
)
from src.domain.enums import SourceSite

load_dotenv()


def _get_bool(value: str | None, default: bool) -> bool:
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


@dataclass(slots=True)
class Settings:
    source_site: SourceSite
    base_url: str
    start_scraping_url: str
    headless: bool
    db_path: Path
    log_level: str
    log_file_path: Path


def load_settings() -> Settings:
    source_site = SourceSite(
        os.getenv("SOURCE_SITE", SourceSite.OXYLABS_SANDBOX.value)
    )
    source_name = source_site.value

    return Settings(
        source_site=source_site,
        base_url=os.getenv("BASE_URL", DEFAULT_BASE_URL),
        start_scraping_url=os.getenv("START_SCRAPING_URL", DEFAULT_SCRAP_URL),
        headless=_get_bool(os.getenv("HEADLESS"), DEFAULT_HEADLESS),
        db_path=Path(
            os.getenv("DB_PATH", str(DB_OUTPUT_DIR / f"{source_name}_scraper.db"))
        ),
        log_level=os.getenv("LOG_LEVEL", DEFAULT_LOG_LEVEL),
        log_file_path=Path(
            os.getenv("LOG_FILE_PATH", str(LOGS_DIR / f"{source_name}_scraper.log"))
        ),
    )
