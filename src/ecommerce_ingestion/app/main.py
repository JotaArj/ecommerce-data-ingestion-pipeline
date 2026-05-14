from ecommerce_ingestion.app.run_catalog import run_catalog
from ecommerce_ingestion.config.settings import load_settings
from ecommerce_ingestion.db.init_db import initialize_database_if_missing


def main() -> None:
    settings = load_settings()
    initialize_database_if_missing(settings)
    run_catalog(settings)


if __name__ == "__main__":
    main()
