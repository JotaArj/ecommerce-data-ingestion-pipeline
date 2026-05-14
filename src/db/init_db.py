from src.config.constants import PROJECT_ROOT
from src.config.settings import load_settings
from src.db.sqlite import build_database


def main() -> None:
    settings = load_settings()
    database = build_database(settings)

    schema_path = PROJECT_ROOT / "src" / "scraper_engine" / "infra" / "db" / "schema.sql"  # noqa: E501
    database.initialize(schema_path)

    print(f"Database initialized at: {database.db_path}")


if __name__ == "__main__":
    main()