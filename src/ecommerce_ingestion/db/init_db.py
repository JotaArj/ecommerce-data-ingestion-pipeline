from ecommerce_ingestion.config.settings import Settings
from ecommerce_ingestion.db.sqlite import build_database


def initialize_database_if_missing(settings: Settings) -> bool:
    database = build_database(settings)
    if database.db_path.exists():
        return False

    database.initialize()
    return True


