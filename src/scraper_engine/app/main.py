from __future__ import annotations

from scraper_engine.application.run_catalog import run_catalog
from scraper_engine.core.settings import load_settings


def main() -> None:
    settings = load_settings()
    run_catalog(settings)


if __name__ == "__main__":
    main()
