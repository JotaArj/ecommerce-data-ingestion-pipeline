from __future__ import annotations

from pathlib import Path

from scraper_engine.domain.enums import SourceSite

PROJECT_ROOT = Path(__file__).resolve().parents[3]

SRC_DIR = PROJECT_ROOT / "src"
DATA_DIR = PROJECT_ROOT / "data"
LOGS_DIR = PROJECT_ROOT / "logs"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

SCREENSHOTS_DIR = ARTIFACTS_DIR / "screenshots"
HTML_DUMPS_DIR = ARTIFACTS_DIR / "html_dumps"

# ==============================================================================
# Source configuration
# ==============================================================================

DEFAULT_SOURCE_SITE = SourceSite.OXYLABS_SANDBOX

SOURCE_BASE_URLS: dict[SourceSite, str] = {
    SourceSite.OXYLABS_SANDBOX: "https://sandbox.oxylabs.io/products",
    SourceSite.WEBSCRAPER_ECOMMERCE_AJAX: (
        "https://webscraper.io/test-sites/e-commerce/ajax"
    ),
}

DEFAULT_BASE_URL = SOURCE_BASE_URLS[DEFAULT_SOURCE_SITE]

# ==============================================================================
# Browser
# ==============================================================================

DEFAULT_HEADLESS = True

DEFAULT_BROWSER_TIMEOUT_MS = 30_000
DEFAULT_NAVIGATION_TIMEOUT_MS = 30_000

DEFAULT_WAIT_AFTER_ACTION_MS = 300

DEFAULT_USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/123.0.0.0 Safari/537.36"
)

# ==============================================================================
# Retry / execution defaults
# ==============================================================================

DEFAULT_RETRY_ATTEMPTS = 3

# límites opcionales para desarrollo/debug
DEFAULT_MAX_CATEGORIES: int | None = None
DEFAULT_MAX_PRODUCTS_PER_LISTING: int | None = None

# ==============================================================================
# Storage / logging defaults
# ==============================================================================

DEFAULT_DB_PATH = DATA_DIR / "scraper.db"

DEFAULT_LOG_FILE_PATH = LOGS_DIR / "scraper.log"
DEFAULT_LOG_LEVEL = "INFO"

# ==============================================================================
# Debug / artifacts
# ==============================================================================

DEFAULT_TAKE_SCREENSHOT_ON_ERROR = True
DEFAULT_SAVE_HTML_ON_ERROR = True

OXYLABS_CATEGORY_START_PATH = "/products/category/"
OXILABS_URL_CATEGORY_PREFIX = "https://oxylabs.io/products/category/"

DEFAULT_SCRAP_URL = "https://sandbox.oxylabs.io/products?page="