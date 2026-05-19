import logging

from ecommerce_ingestion.config.logging_config import configure_logging
from ecommerce_ingestion.config.settings import load_log_settings
from ecommerce_ingestion.processing.gold.build_gold_game_catalog import (
    build_gold_game_catalog,
)

logger = logging.getLogger(__name__)


def run_gold() -> None:
    settings = load_log_settings("gold")
    configure_logging(settings)
    build_gold_game_catalog()


    logger.info("Starting gold data processing.")