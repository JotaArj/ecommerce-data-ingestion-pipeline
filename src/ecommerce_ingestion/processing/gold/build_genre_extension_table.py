import pandas as pd

from ecommerce_ingestion.config.gold_config import (
    GOLD_GENRE_FILENAME,
    GOLD_VALIDATION_CONFIG,
)
from ecommerce_ingestion.config.paths import GOLD_DIR
from ecommerce_ingestion.utils.genre_unifier_service import map_genre
from ecommerce_ingestion.utils.parquet_file_service import save_table
from ecommerce_ingestion.validation.validation_runner import run_validations


class GenreExtensionTable:
    def build(self, data: pd.DataFrame) -> pd.DataFrame:
        data[["mapped_genre", "priority"]] = data["genre_id"].apply(
            lambda x: pd.Series(map_genre(x))
        )
        run_validations(GOLD_GENRE_FILENAME, 
                        data, 
                        GOLD_VALIDATION_CONFIG[GOLD_GENRE_FILENAME] )
        
        save_table(GOLD_GENRE_FILENAME, data, GOLD_DIR)
        return data
