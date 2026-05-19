from ecommerce_ingestion.config.silver_config import (
    SILVER_PRODUCTS_FILENAME,
    SILVER_TABLE_EXPORTS,
)

GOLD_TABLE_IMPORTS: dict[str, str] = SILVER_TABLE_EXPORTS | {
    "game_products": SILVER_PRODUCTS_FILENAME,
}
