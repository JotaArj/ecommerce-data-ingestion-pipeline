import logging

import pandas as pd

logger = logging.getLogger(__name__)

def validate_required_columns(columns: list[str], required_columns: list[str]) -> None:
    if not columns:
        raise ValueError("No columns provided for validation.")

    missing_columns = sorted(set(required_columns) - set(columns))

    if missing_columns:
        raise ValueError(f"Missing required columns: {missing_columns}")

    logger.info("All required silver columns are present.")


def validate_not_empty_dataset(row_count: int) -> None:
    if row_count <= 0:
        raise ValueError("Dataset is empty. Row count must be greater than 0.")
    logger.info(f"Dataset has {row_count} rows, which is valid.")

def critical_null_checker(df: pd.DataFrame, critical_columns: list[str]) -> None: 
    for column in critical_columns:
        null_count = df[column].isnull().sum()
        if null_count > 0:
            raise ValueError(f"Column '{column}' "
                             f"has {null_count} null values, which is not allowed.")
    logger.info("No critical columns contain null values.")

def duplicate_checker(data: pd.DataFrame, subset: list[str]) -> None:
    duplicate_count = data.duplicated(subset=subset).sum()
    if duplicate_count > 0:
        raise ValueError(f"Dataset contains {duplicate_count} "
                         f"duplicate rows based on columns {subset}.")
    logger.info(f"No duplicates found based on columns {subset}.")

def validate_number(data: pd.DataFrame, 
                    column_list: list[str],
                    min_value: float = float('nan'),
                    max_value: float = float('nan')) -> None:
    for column in column_list:
        if min_value is not None:
            below_min_count = (data[column] < min_value).sum()
            if below_min_count > 0:
                raise ValueError(f"Column '{column}' has {below_min_count} "
                                 f"values below the minimum of {min_value}.")
        
        if max_value is not None:
            above_max_count = (data[column] > max_value).sum()
            if above_max_count > 0:
                raise ValueError(f"Column '{column}' has {above_max_count} "
                                 f"values above the maximum of {max_value}.")
    
    logger.info(f"All values in columns {column_list} are within the specified range.")


def unknown_ratio_warning(data: pd.DataFrame, column: str) -> None:
    total_count = len(data)
    unknown_count = (data[column] == "unknown").sum()
    if total_count > 0:
        unknown_ratio = unknown_count / total_count
        logger.warning(f"Column '{column}' has {unknown_count} 'unknown' values "
                       f"out of {total_count} total rows "
                       f"({unknown_ratio:.2%} unknown ratio).")
        