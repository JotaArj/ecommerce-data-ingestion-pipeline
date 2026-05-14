from ecommerce_ingestion.config.settings import Settings, load_settings
from ecommerce_ingestion.db.sqlite import build_database


def initialize_database_if_missing(settings: Settings) -> bool:
    database = build_database(settings)
    if database.db_path.exists():
        return False

    database.initialize()
    return True


def main() -> None:
    settings = load_settings()
    database = build_database(settings)

    created = initialize_database_if_missing(settings)
    status = "created" if created else "already exists"

    print(f"Database {status} at: {database.db_path}")


if __name__ == "__main__":
    main()
