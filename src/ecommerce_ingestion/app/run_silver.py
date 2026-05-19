import logging

from ecommerce_ingestion.config.logging_config import configure_logging
from ecommerce_ingestion.config.settings import load_log_settings
from ecommerce_ingestion.config.silver_config import SILVER_TABLE_EXPORTS
from ecommerce_ingestion.processing.silver.build_silver_direct_database import (
    SilverTableExporter,
)
from ecommerce_ingestion.processing.silver.build_silver_products import (
    SilverProductsBuilder,
)

logger = logging.getLogger(__name__)


def run_silver(run_name: str | None = None) -> None:
    settings = load_log_settings("silver", run_name)
    configure_logging(settings)

    logger.info("Starting silver data processing.")
    SilverProductsBuilder().build()

    for table_name in SILVER_TABLE_EXPORTS:
        SilverTableExporter().build(table_name)

    logger.info("Finished silver data processing.")
