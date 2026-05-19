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
    "genre_id",
    "current_price",
    "currency",
    "stock_status",
    "meta_score",
    "user_score",
    "category_name",
    "category_parent_id",
    "primary_genre",
    "secondary_genre",
    "tertiary_genre"]

GOLD_PRODUCT_COLUMNS_REQUIRED = [
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

GOLD_PRODUCT_CRITICAL_COLUMNS = [
    "game_id",
    "game_name",
    "category_id",
    "current_price",
    "stock_status",
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
    "game_id",
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
    GOLD_GENRE_FILENAME : GOLD_PRODUCT_VALIDATION_CONFIG
}