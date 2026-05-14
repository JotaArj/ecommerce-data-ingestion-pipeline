from src.app.run_catalog import run_catalog
from src.config.settings import load_settings


def main() -> None:
    settings = load_settings()
    run_catalog(settings)


if __name__ == "__main__":
    main()
