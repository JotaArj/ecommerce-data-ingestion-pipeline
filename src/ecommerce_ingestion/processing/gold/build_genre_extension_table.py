import pandas as pd

from ecommerce_ingestion.config.constants import GOLD_DIR
from ecommerce_ingestion.utils.genre_unifier_service import map_genre
from ecommerce_ingestion.utils.parquet_file_service import save_table


class GenreExtensionTable:
    def build(self, data: pd.DataFrame) -> pd.DataFrame:
        data[["mapped_genre", "priority"]] = data["genre_id"].apply(
            lambda x: pd.Series(map_genre(x))
        )
        save_table("gold_game_genre.parquet", data, GOLD_DIR)
        return data