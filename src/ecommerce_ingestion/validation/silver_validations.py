import logging

from ecommerce_ingestion.config.constants import SILVER_COLUMNS_REQUIRED

logger = logging.getLogger(__name__)

def validate_required_columns(columns: list[str]) -> None:
    if not columns:
        raise ValueError("No columns provided for validation.")

    missing_columns = sorted(set(SILVER_COLUMNS_REQUIRED) - set(columns))

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    logger.info("All required silver columns are present.")
    
