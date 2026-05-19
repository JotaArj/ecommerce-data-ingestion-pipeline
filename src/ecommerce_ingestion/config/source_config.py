from ecommerce_ingestion.domain.enums import SourceSite

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
DEFAULT_SCRAPING_URL = "https://sandbox.oxylabs.io/products?page="

OXYLABS_CATEGORY_START_PATH = "/products/category/"
OXYLABS_CATEGORY_URL_PREFIX = "https://oxylabs.io/products/category/"

# Backward-compatible aliases for notebooks and older imports.
OXYLABS_URL_CATEGORY_PREFIX = OXYLABS_CATEGORY_URL_PREFIX
DEFAULT_SCRAP_URL = DEFAULT_SCRAPING_URL
