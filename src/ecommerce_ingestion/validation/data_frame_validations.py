import logging

import pandas as pd

logger = logging.getLogger(__name__)


def validate_required_columns(data: pd.DataFrame, required_columns: list[str]) -> None:
    columns = data.columns.tolist()
    if not columns:
        raise ValueError("No columns provided for validation.")

    missing_columns = sorted(set(required_columns) - set(columns))

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    logger.info("All required columns are present.")


def validate_not_empty_dataset(data: pd.DataFrame) -> None:
    row_count = data.shape[0]
    if row_count <= 0:
        raise ValueError("Dataset is empty. Row count must be greater than 0.")
    logger.info(f"Dataset has {row_count} rows, which is valid.")

def critical_null_checker(data: pd.DataFrame, critical_columns: list[str]) -> None: 
    for column in critical_columns:
        null_count = data[column].isnull().sum()
        if null_count > 0:
            raise ValueError(f"Column '{column}' "
                             f"has {null_count} null values, which is not allowed.")
    logger.info("No critical columns contain null values.")

def duplicate_checker(data: pd.DataFrame, id_column_name: str) -> None:
    duplicate_count = data.duplicated(id_column_name).sum()
    if duplicate_count > 0:
        raise ValueError(f"Dataset contains {duplicate_count} "
                         f"duplicate rows based on columns {id_column_name}.")
    logger.info(f"No duplicates found based on columns {id_column_name}.")

def validate_number(data: pd.DataFrame, 
                    column_name: str,
                    min_value: float | None,
                    max_value: float | None) -> None:

    if min_value is not None:
        below_min_count = (data[column_name] < min_value).sum()
        if below_min_count > 0:
            raise ValueError(f"Column '{column_name}' has {below_min_count} "
                             f"values below the minimum of {min_value}.")
    
    if max_value is not None:
        above_max_count = (data[column_name] > max_value).sum()
        if above_max_count > 0:
            raise ValueError(f"Column '{column_name}' has {above_max_count} "
                             f"values above the maximum of {max_value}.")
    
    logger.info(f"All values in columns {column_name} are within the specified range.")


def unknown_ratio_warning(data: pd.DataFrame, column_list: list[str]) -> None:
    total_count = len(data)
    for column in column_list:
        unknown_count = (data[column] == "unknown").sum()
        if unknown_count > 0 and unknown_count > 0:
            unknown_ratio = unknown_count / total_count
            logger.warning(f"Column '{column}' has {unknown_count} 'unknown' values "
                           f"out of {total_count} total rows "
                           f"({unknown_ratio:.2%} unknown ratio).")
        