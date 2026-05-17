import logging

from ecommerce_ingestion.config.logging_config import configure_logging
from ecommerce_ingestion.config.settings import load_silver_settings
from ecommerce_ingestion.processing.gold.build_gold_products import (
    build_gold_products,
)
from ecommerce_ingestion.processing.silver.build_silver_direct_database import (
    build_silver_direct_database,
)

logger = logging.getLogger(__name__)


def run_gold() -> None:
    settings = load_gold_settings()
    configure_logging(settings)


    logger.info("Starting gold data processing.")