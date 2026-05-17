from pathlib import Path

from ecommerce_ingestion.domain.enums import SourceSite

SILVER_SELECT_COLUMNS = [
    "p.game_id",
    "p.game_source_site",
    "p.source_game_product_code",
    "p.game_name",
    "p.game_product_type",
    "p.game_rating",
    "p.game_pdp_url",
    "p.game_developer",
    "p.game_description",
    "g.genres",
    "gpc.category_id",
    "gc.category_source_site",
    "gc.source_category_code",
    "gc.category_name",
    "gc.category_url",
    "gc.category_path",
    "gc.category_parent_id",
    "gc.category_level",
    "gc.category_is_leaf",
    "gpsl.current_price",
    "gpsl.currency",
    "gpsl.stock_status",
    "gpsl.meta_score",
    "gpsl.user_score",
]

SILVER_COLUMNS_REQUIRED = [
    "game_id",
    "game_source_site",
    "source_game_product_code",
    "game_name",
    "game_product_type",
    "game_rating",
    "game_pdp_url",
    "game_developer",
    "game_description",
    "genres",
    "category_id",
    "category_source_site",
    "source_category_code",
    "category_name",
    "category_url",
    "category_path",
    "category_parent_id",
    "category_level",
    "category_is_leaf",
    "current_price",
    "currency",
    "stock_status",
    "meta_score",
    "user_score",
]

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"
BRONZE_DIR = DATA_DIR / "raw"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
LOGS_DIR = DATA_DIR / "logs"

BRONZE_DATABASE_FILENAME = "oxylabs_sandbox_scraper.db"

SILVER_PRODUCTS_FILENAME = "silver_cleaned_data.parquet"
SILVER_TABLE_EXPORTS: dict[str, str] = {
    "game_genre_game_link": "silver_game_genre_relationships.parquet",
    "game_product_snapshots": "silver_snapshots.parquet",
}

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
OXYLABS_CATEGORY_URL_PREFIX = "https://oxylabs.io/products/category/"

DEFAULT_SCRAPING_URL = "https://sandbox.oxylabs.io/products?page="

# Backward-compatible aliases for notebooks and older imports.
DB_OUTPUT_DIR = DATA_DIR
DB_OUTPUT_BRONZE = BRONZE_DIR
DB_OUTPUT_SILVER = SILVER_DIR
DB_OUTPUT_GOLD = GOLD_DIR
OXYLABS_URL_CATEGORY_PREFIX = OXYLABS_CATEGORY_URL_PREFIX
DEFAULT_SCRAP_URL = DEFAULT_SCRAPING_URL
