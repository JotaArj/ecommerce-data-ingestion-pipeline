import logging

import pandas as pd

from ecommerce_ingestion.config.constants import DB_OUTPUT_SILVER, DB_OUTPUT_GOLD
from ecommerce_ingestion.db.sql_clauses import PRODUCT_QUERY_JOINED

logger = logging.getLogger(__name__)

class build_gold_genre_performance:
    def build(self) -> None:
        logger.info("Starting to build silver products dataset.")
        try:
            data_products = pd.read_parquet(DB_OUTPUT_SILVER / "silver_cleaned_data.parquet")
            logging.info(f"Columns in cleaned data: {data_products.columns.tolist()}")
        except Exception as e:
            logger.error(f"Error while reading silver_cleaned_data parquet file: {e}")