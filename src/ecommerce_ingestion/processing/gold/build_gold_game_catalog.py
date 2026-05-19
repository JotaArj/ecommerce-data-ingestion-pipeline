import logging

import pandas as pd

logger = logging.getLogger(__name__)
class GoldGameCatalogBuilder:
    def build(self, data_dict: dict[str, pd.DataFrame]) -> pd.DataFrame:
        logger.info("Starting to build silver products dataset.")
        ## joinear links con genre_extension
        ## dropear duplicados id, mapped_genre
        ## Rankear pr game_id, y priority
        ## Descartar ranks 4 o mas
        ## pivotar tabla para obtener los 3 generos principales
        ## rellenar con unknowns lo que salga nulo
        ## joinear tabla con products
        ## salvar tabla completa
        ## dropear columnas innecesarias
        ## crear score y price bucket
        ## salvar tabla final
        data = pd.DataFrame
        return data
    

    
    
    
