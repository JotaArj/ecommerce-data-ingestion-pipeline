from pathlib import Path

from ecommerce_ingestion.domain.enums import SourceSite

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DB_OUTPUT_DIR = PROJECT_ROOT / "data"
DB_OUTPUT_BRONZE = DB_OUTPUT_DIR / "raw"
DB_OUTPUT_SILVER = DB_OUTPUT_DIR / "silver"
DB_OUTPUT_GOLD = DB_OUTPUT_DIR / "gold"


LOGS_DIR = DB_OUTPUT_DIR / "logs"

SOURCE_BASE_URLS: dict[SourceSite, str] = {
    SourceSite.OXYLABS_SANDBOX: "https://sandbox.oxylabs.io/products",
    SourceSite.WEBSCRAPER_ECOMMERCE_AJAX: (
        "https://webscraper.io/test-sites/e-commerce/ajax"
    ),
}

DEFAULT_SOURCE_SITE = SourceSite.OXYLABS_SANDBOX
DEFAULT_BASE_URL = SOURCE_BASE_URLS[SourceSite.OXYLABS_SANDBOX]

DEFAULT_HEADLESS = True
DEFAULT_LOG_LEVEL = "INFO"

OXYLABS_CATEGORY_START_PATH = "/products/category/"
OXYLABS_URL_CATEGORY_PREFIX = "https://oxylabs.io/products/category/"

DEFAULT_SCRAP_URL = "https://sandbox.oxylabs.io/products?page="
