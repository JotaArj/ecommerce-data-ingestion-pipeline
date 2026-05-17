import logging
import sqlite3

import pandas as pd

from ecommerce_ingestion.config.constants import DB_OUTPUT_BRONZE, DB_OUTPUT_SILVER
from ecommerce_ingestion.db.sql_clauses import PRODUCT_QUERY_JOINED

logger = logging.getLogger(__name__)

class build_silver_products:
    def __init__(self) -> None:
        try:
            self.conn_bronze = sqlite3.connect(DB_OUTPUT_BRONZE / 
                                               "oxylabs_sandbox_scraper.db")
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

        logger.info(f"Readed {data_products.shape[0]} rows"
                    f" and {data_products.shape[1]} columns.")


        logger.info("Starting to build silver products dataset.")

        try:
            data_products = data_products.fillna({
                "game_product_type": "unknown",
                "game_rating": "unknown",
                "game_developer": "unknown",
                "category_parent_id": "none",
            })
        except Exception as e:
            logger.error(f"Error while filling missing values: {e}")
            self.close_connections()
            raise
        
        logger.info("Normalize id fields to lowercase.")
        data_products["game_id"] = data_products["game_id"].str.lower()
        data_products["game_developer"] = data_products["game_developer"].str.lower()

        try:
            data_products.to_parquet(DB_OUTPUT_SILVER / "silver_cleaned_data.parquet", 
                                    index=False)
        except Exception as e:
            logger.error(f"Error while saving cleaned data: {e}")
            self.close_connections()
            raise

        logger.info(f"Saved silver_cleaned_data parquet file correctly." 
            f" Total saved: {data_products.shape[0]} rows, {data_products.shape[1]} columns.")
        self.close_connections()



    def close_connections(self) -> None:
        try:
            self.conn_bronze.close()
        except Exception as e:
            logger.error(f"Error while closing sqlite connection: {e}")
            raise
