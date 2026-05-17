#from ecommerce_ingestion.app.run_catalog import run_catalog
#from ecommerce_ingestion.config.constants import DEFAULT_SOURCE_SITE
from ecommerce_ingestion.app.run_silver import run_silver


def main() -> None:

    #run_catalog(DEFAULT_SOURCE_SITE)
    run_silver()



if __name__ == "__main__":
    main()
