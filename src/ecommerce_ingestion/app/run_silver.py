import logging

from ecommerce_ingestion.config.constants import SILVER_TABLE_EXPORTS
from ecommerce_ingestion.config.logging_config import configure_logging
from ecommerce_ingestion.config.settings import load_silver_settings
from ecommerce_ingestion.processing.silver.build_silver_direct_database import (
    SilverTableExporter,
)
from ecommerce_ingestion.processing.silver.build_silver_products import (
    SilverProductsBuilder,
)
from ecommerce_ingestion.validation.silver_validations import (
    run_silver_validations,
)

logger = logging.getLogger(__name__)


def run_silver() -> None:
    settings = load_silver_settings()
    configure_logging(settings)

    logger.info("Starting silver data processing.")
    SilverProductsBuilder().build()

    for table_name in SILVER_TABLE_EXPORTS:
        SilverTableExporter().build(table_name)

    run_silver_validations()

    logger.info("Finished silver data processing.")
