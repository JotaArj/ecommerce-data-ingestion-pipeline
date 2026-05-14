from src.app.run_catalog import run_catalog
from src.config.settings import load_settings
from src.db.init_db import initialize_database_if_missing


def main() -> None:
    settings = load_settings()
    initialize_database_if_missing(settings)
    run_catalog(settings)


if __name__ == "__main__":
    main()
