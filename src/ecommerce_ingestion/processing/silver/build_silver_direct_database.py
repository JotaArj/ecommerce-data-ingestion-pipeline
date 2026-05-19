import logging
import sqlite3

import pandas as pd

from ecommerce_ingestion.config.paths import (
    BRONZE_DATABASE_FILENAME,
    BRONZE_DIR,
    SILVER_DIR,
)
from ecommerce_ingestion.config.silver_config import (
    SILVER_TABLE_EXPORTS,
)

logger = logging.getLogger(__name__)


class SilverTableExporter:
    def __init__(self) -> None:
        self.conn_bronze = sqlite3.connect(BRONZE_DIR / BRONZE_DATABASE_FILENAME)

    def build(self, database_table: str) -> None:
        if database_table not in SILVER_TABLE_EXPORTS:
            raise ValueError(f"Unsupported silver export table: {database_table}")

        output_filename = SILVER_TABLE_EXPORTS[database_table]
        logger.info(f"Starting to build silver {database_table} links dataset.")
        try:
            data = pd.read_sql(f"SELECT * FROM {database_table}", self.conn_bronze)
        except Exception as e:
            logger.error(f"Error while executing SQL query on {database_table}: {e}")
            self.close_connections()
            raise

        logger.info(f"Read {data.shape[0]} rows from {database_table}.")

        try:
            SILVER_DIR.mkdir(parents=True, exist_ok=True)
            data.to_parquet(SILVER_DIR / output_filename, index=False)
        except Exception as e:
            logger.error(f"Error while saving cleaned data on {database_table}: {e}")
            self.close_connections()
            raise

        logger.info(
            f"Saved silver {output_filename} parquet file correctly."
            f" Total saved: {data.shape[0]} rows, {data.shape[1]} columns."
        )
        self.close_connections()

    def close_connections(self) -> None:
        try:
            self.conn_bronze.close()
        except Exception as e:
            logger.error(f"Error while closing sqlite connection: {e}")
            raise
