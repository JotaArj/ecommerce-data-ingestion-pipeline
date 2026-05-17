import logging

from ecommerce_ingestion.config.logging_config import configure_logging
from ecommerce_ingestion.config.settings import load_silver_settings
from ecommerce_ingestion.processing.silver.build_silver_direct_database import (
    build_silver_direct_database,
)
from ecommerce_ingestion.processing.silver.build_silver_products import (
    build_silver_products,
)

logger = logging.getLogger(__name__)


def run_silver() -> None:
    settings = load_silver_settings()
    configure_logging(settings)


    logger.info("Starting silver data processing.")
    build_silver_products().build()
    build_silver_direct_database().build("game_genre_game_link", 
                                         "silver_game_genre_relationships")
    build_silver_direct_database().build("game_product_snapshots",
                                         "silver_snapshots")