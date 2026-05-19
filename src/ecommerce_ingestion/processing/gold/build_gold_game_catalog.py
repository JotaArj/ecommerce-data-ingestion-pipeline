import logging

import pandas as pd

from ecommerce_ingestion.config.gold_config import (
    GOLD_GAME_DATA_COLUMN_LIST,
    GOLD_PRODUCT_FILENAME,
    GOLD_VALIDATION_CONFIG,
)
from ecommerce_ingestion.config.paths import GOLD_DIR
from ecommerce_ingestion.utils.bucket_service import (
    build_price_bucket,
    build_score_bucket,
)
from ecommerce_ingestion.utils.parquet_file_service import save_table
from ecommerce_ingestion.validation.validation_runner import run_validations

logger = logging.getLogger(__name__)
class GoldGameCatalogBuilder:
    def build(self, data_dict: dict[str, pd.DataFrame]) -> pd.DataFrame:
        logger.info("Starting to build silver products dataset.")

        data_genre = data_dict["game_genre_game_link"].merge(
            data_dict["game_genre_extension"],
            left_on="genre_id",
            right_on="genre_id",
            how="left"
        )

        data_genre = data_genre.drop_duplicates(["genre_id", "mapped_genre"])
        
        data_genre = data_genre.sort_values(["game_id", "priority"])
        data_genre["genre_rank"] = (
            data_genre
            .groupby("game_id")
            .cumcount() + 1
        )

        data_genre = data_genre[data_genre["genre_rank"] <= 3]
        data_genre = (
            data_genre
            .pivot(
                index="game_id",
                columns="genre_rank",
                values="mapped_genre"
            )
            .rename(columns={
                1: "primary_genre",
                2: "secondary_genre",
                3: "tertiary_genre"
            })
            .reset_index()
        )
        data_genre = data_genre.fillna("unknown")

        gold_game_catalog = data_dict["game_products"].merge(
            data_genre,
            on="game_id", 
            how="left")
        
        save_table("gold_all_columns_game_catalog.parquet", gold_game_catalog, GOLD_DIR)

        gold_game_catalog = gold_game_catalog[GOLD_GAME_DATA_COLUMN_LIST]
        gold_game_catalog["price_bucket"] = (
            gold_game_catalog["current_price"]
            .apply(build_price_bucket)
        )

        gold_game_catalog["score_bucket"] = (
            gold_game_catalog["meta_score"]
            .apply(build_score_bucket)
        )

        run_validations(GOLD_PRODUCT_FILENAME, 
                        gold_game_catalog, 
                        GOLD_VALIDATION_CONFIG[GOLD_PRODUCT_FILENAME])
        save_table(GOLD_PRODUCT_FILENAME, gold_game_catalog, GOLD_DIR)
        return gold_game_catalog
    

    
    
    
