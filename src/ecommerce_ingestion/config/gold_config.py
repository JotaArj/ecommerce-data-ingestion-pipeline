from ecommerce_ingestion.config.silver_config import (
    SILVER_PRODUCTS_FILENAME,
    SILVER_TABLE_EXPORTS,
)
from ecommerce_ingestion.domain.models import ValidationConfig

GOLD_GENRE_FILENAME = "gold_game_genre.parquet"
GOLD_PRODUCT_FILENAME = "gold_game_catalog.parquet"

GOLD_TABLE_IMPORTS: dict[str, str] = SILVER_TABLE_EXPORTS | {
    "game_products": SILVER_PRODUCTS_FILENAME,
}

GOLD_GAME_DATA_COLUMN_LIST = [
    "game_id",
    "game_name",
    "game_developer",
    "game_rating",
    "game_product_type",
    "genres",
    "current_price",
    "currency",
    "stock_status",
    "meta_score",
    "user_score",
    "category_name",
    "category_parent_id",
    "primary_genre",
    "secondary_genre"]

GOLD_PRODUCT_COLUMNS_REQUIRED = [
    "game_id",
    "game_name",
    "game_developer",
    "game_rating",
    "game_product_type",
    "genres",
    "current_price",
    "currency",
    "stock_status",
    "meta_score",
    "user_score",
    "category_name",
    "category_parent_id",
    "primary_genre",
    "secondary_genre",
    "price_bucket",
    "score_bucket"
]

GOLD_PRODUCT_CRITICAL_COLUMNS = [
    "game_id",
    "game_name",
    "primary_genre",
    "current_price",
    "meta_score",
    "user_score",
    "stock_status",
    "category_name"
]

DEFAULT_UNKNOWN_RATIO_THRESHOLD = 0.5

GOLD_PRODUCT_NUMERIC_COLUMNS_VALUES: list[tuple[str, float | None, float | None]] = [
        ("current_price", 0.0, None),
        ("user_score", 0.0, None),
        ("meta_score", 0.0, None)
]

GOLD_PRODUCT_VALIDATION_CONFIG: ValidationConfig = {
    "required_columns" : GOLD_PRODUCT_COLUMNS_REQUIRED,
    "critical_null_columns" : GOLD_PRODUCT_CRITICAL_COLUMNS,
    "id_columns": "game_id",
    "number_column_list": GOLD_PRODUCT_NUMERIC_COLUMNS_VALUES
}

GOLD_GENRE_DATA_COLUMN_LIST = [
    "genre_id",
    "mapped_genre",
    "priority"
]

GOLD_GENRE_NUMERIC_COLUMNS_VALUES: list[tuple[str, float | None, float | None]] = [
        ("priority", 0.0, 999.0)
]

GOLD_GENRE_VALIDATION_CONFIG: ValidationConfig = {
    "required_columns" : GOLD_GENRE_DATA_COLUMN_LIST,
    "critical_null_columns" : GOLD_GENRE_DATA_COLUMN_LIST,
    "id_columns": "genre_id",
    "number_column_list": GOLD_GENRE_NUMERIC_COLUMNS_VALUES
}

GOLD_VALIDATION_CONFIG: dict[str, ValidationConfig]= {
    GOLD_PRODUCT_FILENAME : GOLD_PRODUCT_VALIDATION_CONFIG,
    GOLD_GENRE_FILENAME : GOLD_GENRE_VALIDATION_CONFIG
}