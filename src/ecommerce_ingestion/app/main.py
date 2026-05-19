from ecommerce_ingestion.app.run_catalog import run_catalog
from ecommerce_ingestion.app.run_gold import run_gold
from ecommerce_ingestion.app.run_silver import run_silver
from ecommerce_ingestion.config.source_config import DEFAULT_SOURCE_SITE


def main() -> None:

    run_catalog(DEFAULT_SOURCE_SITE)
    run_silver()
    run_gold()



if __name__ == "__main__":
    main()
