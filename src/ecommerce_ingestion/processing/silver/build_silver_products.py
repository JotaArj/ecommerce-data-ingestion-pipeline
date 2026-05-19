import logging
import sqlite3

import pandas as pd

from ecommerce_ingestion.config.constants import (
    BRONZE_DATABASE_FILENAME,
    BRONZE_DIR,
    SILVER_DIR,
    SILVER_PRODUCTS_FILENAME,
)
from ecommerce_ingestion.db.sql_clauses import PRODUCT_QUERY_JOINED
from ecommerce_ingestion.validation.validation_runner import run_silver_validations

logger = logging.getLogger(__name__)


class SilverProductsBuilder:
    def __init__(self) -> None:
        try:
            self.conn_bronze = sqlite3.connect(BRONZE_DIR / BRONZE_DATABASE_FILENAME)
        except Exception as e:
            logger.error(f"Error while connecting to raw database: {e}")
            raise

    def build(self) -> None:
        logger.info("Starting to build silver products dataset.")

        try:
            data_products = pd.read_sql(PRODUCT_QUERY_JOINED, self.conn_bronze)
        except Exception as e:
            logger.error(f"Error while executing SQL query: {e}")
            self.close_connections()
            raise

        logger.info(
            "Read %s rows and %s columns.",
            data_products.shape[0],
            data_products.shape[1],
        )

        logger.info("Cleaning silver products dataset.")

        try:
            data_products = data_products.fillna(
                {
                    "game_product_type": "unknown",
                    "game_rating": "unknown",
                    "game_developer": "unknown",
                    "category_parent_id": "root"
                }
            )
        except Exception as e:
            logger.error(f"Error while filling missing values: {e}")
            self.close_connections()
            raise

        logger.info("Normalize id fields to lowercase.")
        data_products["game_id"] = data_products["game_id"].str.lower()
        data_products["game_developer"] = data_products["game_developer"].str.lower()

        try:
            SILVER_DIR.mkdir(parents=True, exist_ok=True)
            data_products.to_parquet(SILVER_DIR / SILVER_PRODUCTS_FILENAME, index=False)
        except Exception as e:
            logger.error(f"Error while saving cleaned data: {e}")
            self.close_connections()
            raise

        run_silver_validations(data_products)

        logger.info(
            "Saved %s correctly. Total saved: %s rows, %s columns.",
            SILVER_PRODUCTS_FILENAME,
            data_products.shape[0],
            data_products.shape[1],
        )
        self.close_connections()

    def close_connections(self) -> None:
        try:
            self.conn_bronze.close()
        except Exception as e:
            logger.error(f"Error while closing sqlite connection: {e}")
            raise


build_silver_products = SilverProductsBuilder
