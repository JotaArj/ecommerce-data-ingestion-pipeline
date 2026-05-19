import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

def load_table(nametable: str, data_path: Path) -> pd.DataFrame:
    try:
        data = pd.read_parquet(data_path)
        logger.info(f"Columns in {nametable} data: "
                     f"{data.columns.tolist()}")
        return data
    except Exception as e:
        logger.error(f"Error while reading {nametable} parquet file: {e}")
        raise


def save_table(data_table_name: str, data: pd.DataFrame, dir_path: Path) -> None:
    try:
        data.to_parquet(dir_path, index= False)
        logger.info(f"{data_table_name} data: correctly saved")
    except Exception as e:
        logger.error(f"Error while reading {data_table_name} parquet file: {e}")
        raise

def load_dict_table(table_dict: dict[str,str]
                    , path_dir: Path) -> dict[str, pd.DataFrame]:
    data_dict = {}
    for name_table, table_path in table_dict.items():
        data_dict[name_table] = load_table(name_table, 
                                           path_dir / table_path)
    return data_dict
