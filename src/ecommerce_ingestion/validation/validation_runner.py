import logging

import pandas as pd

from ecommerce_ingestion.config.constants import SILVER_COLUMNS_REQUIRED
from ecommerce_ingestion.validation.silver_validations import (
    critical_null_checker,
    duplicate_checker,
    unknown_ratio_warning,
    validate_not_empty_dataset,
    validate_number,
    validate_required_columns,
)

logger = logging.getLogger(__name__)

def run_silver_validations(data: pd.DataFrame) -> None:
    logger.info("Starting silver data validations.")
    try:
        validate_required_columns(data.columns.tolist(), SILVER_COLUMNS_REQUIRED)
        validate_not_empty_dataset(len(data))
        critical_null_checker(data, SILVER_COLUMNS_REQUIRED)
        duplicate_checker(data, ["game_id","category_id"])
        validate_number(data, 
                        ["current_price", "user_score", "meta_score"], 
                        min_value=0)
        unknown_ratio_warning(data, data.columns)
    except Exception as e:
        logger.error(f"Silver data validation failed: {e}")
        raise

    logger.info("Finished silver data validations.")

def run_gold_validations(data: pd.DataFrame) -> None:
    logger.info("Starting silver data validations.")
    try:
        validate_required_columns(data.columns.tolist(), SILVER_COLUMNS_REQUIRED)
        validate_not_empty_dataset(len(data))
        critical_null_checker(data, SILVER_COLUMNS_REQUIRED)
        duplicate_checker(data, ["game_id","category_id"])
        validate_number(data, 
                        ["current_price", "user_score", "meta_score"], 
                        min_value=0)
        unknown_ratio_warning(data, data.columns)
    except Exception as e:
        logger.error(f"Silver data validation failed: {e}")
        raise
    logger.info("Finished silver data validations.")
