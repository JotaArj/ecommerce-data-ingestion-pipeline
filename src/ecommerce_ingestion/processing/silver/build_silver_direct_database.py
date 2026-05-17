import logging
import sqlite3

import pandas as pd

from ecommerce_ingestion.config.constants import DB_OUTPUT_BRONZE, DB_OUTPUT_SILVER

logger = logging.getLogger(__name__)

class build_silver_direct_database:
    def __init__(self) -> None:
        self.conn_bronze = sqlite3.connect(DB_OUTPUT_BRONZE / 
                                               "oxylabs_sandbox_scraper.db")

    def build(self, database_table: str, name: str) -> None:
        logger.info(f"Starting to build silver {database_table} links dataset.")
        try:
            data = pd.read_sql(f"SELECT * FROM {database_table}", 
                                        self.conn_bronze)
        except Exception as e:
            logger.error(f"Error while executing SQL query on {database_table}: {e}")
            self.close_connections()
            raise
        
        logger.info(f"Readed {data.shape[0]} rows from {database_table}.")

        try:
            data.to_parquet(DB_OUTPUT_SILVER / f"{name}.parquet", 
                                    index=False)
        except Exception as e:
            logger.error(f"Error while saving cleaned data on {database_table}: {e}")
            self.close_connections()
            raise

        logger.info(f"Saved silver {name} parquet file correctly." 
                    f" Total saved: {data.shape[0]} rows, {data.shape[1]} columns.")
        self.close_connections()

    def close_connections(self) -> None:
        try:
            self.conn_bronze.close()
        except Exception as e:
            logger.error(f"Error while closing sqlite connection: {e}")
            raise