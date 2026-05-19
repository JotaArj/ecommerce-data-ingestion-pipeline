import logging

from ecommerce_ingestion.config.constants import (
    GOLD_TABLE_IMPORTS,
    SILVER_DIR,
)
from ecommerce_ingestion.config.logging_config import configure_logging
from ecommerce_ingestion.config.settings import load_log_settings
from ecommerce_ingestion.processing.gold.build_genre_extension_table import (
    GenreExtensionTable,
)
from ecommerce_ingestion.processing.gold.build_gold_game_catalog import (
    GoldGameCatalogBuilder,
)
from ecommerce_ingestion.utils.parquet_file_service import load_dict_table

logger = logging.getLogger(__name__)


def run_gold() -> None:
    settings = load_log_settings("gold")
    configure_logging(settings)
    game_catalog_builder = GoldGameCatalogBuilder()
    genre_extension_builder = GenreExtensionTable()
    table_dict = load_dict_table(GOLD_TABLE_IMPORTS, SILVER_DIR)
    table_dict["game_genre_extension"] = genre_extension_builder.build(
        table_dict["game_genre"])
    data_game_catalog = game_catalog_builder.build(table_dict)

    logger.info("Starting gold data processing.")