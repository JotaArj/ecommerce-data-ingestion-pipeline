import logging

import pandas as pd

from ecommerce_ingestion.domain.models import ValidationConfig
from ecommerce_ingestion.validation.data_frame_validations import (
    critical_null_checker,
    duplicate_checker,
    unknown_ratio_warning,
    validate_not_empty_dataset,
    validate_number,
    validate_required_columns,
)

logger = logging.getLogger(__name__)

def run_validations(table_name: str, 
                    data: pd.DataFrame, 
                    validation_config: ValidationConfig) -> None:
    logger.info(f"Starting {table_name} validations.")
    try:
        validate_required_columns(data, 
                                  validation_config["required_columns"])
        validate_not_empty_dataset(data)
        critical_null_checker(data, validation_config["critical_null_columns"])
        duplicate_checker(data, validation_config["id_columns"])
        for column in validation_config["number_column_list"]:
            validate_number(data, column[0], column[1], column[2])
        unknown_ratio_warning(data, data.columns.to_list())
    except Exception as e:
        logger.error(f"{table_name} validation failed: {e}")
        raise

    logger.info("Finished {table_name} validations.")