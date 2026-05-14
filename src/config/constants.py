from pathlib import Path

from src.domain.enums import SourceSite

PROJECT_ROOT = Path(__file__).resolve().parents[2]

LOGS_DIR = PROJECT_ROOT / "logs"
DB_OUTPUT_DIR = PROJECT_ROOT / "db" / "output"

SOURCE_BASE_URLS: dict[SourceSite, str] = {
    SourceSite.OXYLABS_SANDBOX: "https://sandbox.oxylabs.io/products",
    SourceSite.WEBSCRAPER_ECOMMERCE_AJAX: (
        "https://webscraper.io/test-sites/e-commerce/ajax"
    ),
}

DEFAULT_BASE_URL = SOURCE_BASE_URLS[SourceSite.OXYLABS_SANDBOX]

DEFAULT_HEADLESS = True
DEFAULT_LOG_LEVEL = "INFO"

OXYLABS_CATEGORY_START_PATH = "/products/category/"
OXILABS_URL_CATEGORY_PREFIX = "https://oxylabs.io/products/category/"

DEFAULT_SCRAP_URL = "https://sandbox.oxylabs.io/products?page="
