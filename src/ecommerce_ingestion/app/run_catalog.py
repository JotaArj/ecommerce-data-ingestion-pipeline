import logging
from datetime import datetime
from logging.handlers import RotatingFileHandler
from math import ceil
from uuid import uuid4

from playwright.sync_api import Page

from ecommerce_ingestion.browser.playwright_factory import PlaywrightFactory
from ecommerce_ingestion.config.constants import OXILABS_URL_CATEGORY_PREFIX
from ecommerce_ingestion.config.settings import Settings
from ecommerce_ingestion.db.repositories import (
    CategoryRepository,
    ProductCategoryRepository,
    ProductRepository,
    ProductSnapshotRepository,
    RunRepository,
)
from ecommerce_ingestion.db.sqlite import SQLiteDatabase, build_database
from ecommerce_ingestion.domain.enums import RunStatus, RunType, SourceSite
from ecommerce_ingestion.domain.models import (
    CategoryNode,
    Product,
    ProductCategoryLink,
    ProductSnapshot,
    ScraperRun,
)
from ecommerce_ingestion.sources.oxylabs.discovery import Discovery
from ecommerce_ingestion.sources.oxylabs.scraper import Scraper
from ecommerce_ingestion.sources.oxylabs.selectors import PRICE_SELECTOR

logger = logging.getLogger(__name__)


def run_catalog(settings: Settings) -> None:
    _configure_logging(settings)
    database = build_database(settings)
    run = ScraperRun(
        id=str(uuid4()),
        run_type=RunType.CATALOG,
        source_site=settings.source_site,
        status=RunStatus.RUNNING,
        started_at=datetime.now(),
    )
    _save_run(database, run)

    logger.info("Starting catalog run %s", run.id)
    total_products = 0
    total_snapshots = 0
    total_links = 0
    try:
        with PlaywrightFactory(settings) as factory:
            with factory.page_session() as page:
                with database.session() as connection:
                    category_repository = CategoryRepository(connection)
                    product_category_repository = ProductCategoryRepository(connection)
                    product_snapshot_repository = ProductSnapshotRepository(connection)
                    product_repository = ProductRepository(connection)

                    category_nodes = _discover_categories(settings, page)
                    logger.info("Discovered %s categories", len(category_nodes))
                    for category_node in category_nodes:
                        category_repository.upsert(category_node)

                    json = capture_products_json_from_navigation(settings, page, 1)
                    total_pages, products_per_page = _capture_atributes_from_json(json)
                    logger.info(
                        "Catalog has %s pages with %s products per page",
                        total_pages,
                        products_per_page,
                    )

                    for page_number in range(1, total_pages + 1):
                        json = capture_products_json_from_navigation(
                            settings, page, page_number
                        )
                        (
                            products,
                            product_snapshots,
                            product_category_links,
                        ) = _discover_products_from_json(page, run.id, json)

                        for product in products:
                            product_repository.upsert(product)

                        for product_category_link in product_category_links:
                            _ensure_category_exists(
                                category_repository,
                                settings,
                                product_category_link.category_id,
                            )
                            product_category_repository.upsert(product_category_link)

                        for product_snapshot in product_snapshots:
                            product_snapshot_repository.insert(product_snapshot)

                        total_products += len(products)
                        total_snapshots += len(product_snapshots)
                        total_links += len(product_category_links)
                        logger.info(
                            "Processed page %s: %s products, %s snapshots, %s links",
                            page_number,
                            len(products),
                            len(product_snapshots),
                            len(product_category_links),
                        )

        run.status = RunStatus.SUCCEEDED
        run.finished_at = datetime.now()
        _save_run(database, run)
        logger.info(
            "Catalog run %s succeeded: %s products, %s snapshots, %s links",
            run.id,
            total_products,
            total_snapshots,
            total_links,
        )
    except Exception as exc:
        run.status = RunStatus.FAILED
        run.finished_at = datetime.now()
        run.error_message = str(exc)
        _save_run(database, run)
        logger.exception("Catalog run %s failed", run.id)
        raise


def _configure_logging(settings: Settings) -> None:
    settings.log_file_path.parent.mkdir(parents=True, exist_ok=True)
    root_logger = logging.getLogger()
    root_logger.handlers.clear()
    root_logger.setLevel(settings.log_level)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler = RotatingFileHandler(
        settings.log_file_path,
        maxBytes=10 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(settings.log_level)
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def _save_run(database: SQLiteDatabase, run: ScraperRun) -> None:
    with database.session() as connection:
        RunRepository(connection).upsert(run)


def _discover_categories(settings: Settings, page: Page) -> list[CategoryNode]:
    page.goto(settings.base_url, wait_until="domcontentloaded")
    return _discover_categories_for_source(page, settings)


def _discover_categories_for_source(
    page: Page, settings: Settings
) -> list[CategoryNode]:
    if settings.source_site is SourceSite.OXYLABS_SANDBOX:
        scraper = Scraper(page)
        scraper.expand_category_menu()

        discovery = Discovery(page)
        return discovery.discover_categories()

    raise NotImplementedError(
        f"Catalog runner not implemented for source site: {settings.source_site}"
    )


def capture_products_json_from_navigation(
    settings: Settings, page: Page, num_page: int
) -> dict[str, object]:
    with page.expect_response(
        lambda response: "/api/products" in response.url
    ) as response_info:
        page.goto(
            settings.start_scraping_url + str(num_page),
            wait_until="networkidle",
        )

    response = response_info.value
    payload: object = response.json()
    if not isinstance(payload, list):
        raise ValueError("Expected products API response to be a list")

    products: list[object] = payload
    products_per_page = page.locator(PRICE_SELECTOR).count()
    if products_per_page <= 0:
        raise ValueError("Could not detect visible products per page")

    start = (num_page - 1) * products_per_page
    end = start + products_per_page
    return {
        "pageProps": {
            "pageCount": ceil(len(products) / products_per_page),
            "perPage": products_per_page,
            "products": products[start:end],
        }
    }


def _capture_atributes_from_json(json: dict[str, object]) -> tuple[int, int]:
    page_props: object = json["pageProps"]
    if not isinstance(page_props, dict):
        raise ValueError("Expected pageProps to be an object")

    page_count: object = page_props["pageCount"]
    per_page: object = page_props["perPage"]
    if not isinstance(page_count, int) or not isinstance(per_page, int):
        raise ValueError("Expected pageCount and perPage to be integers")

    return page_count, per_page


def _discover_products_from_json(
    page: Page, run_id: str, json: dict[str, object]
) -> tuple[list[Product], list[ProductSnapshot], list[ProductCategoryLink]]:
    discovery = Discovery(page)

    return discovery.discover_products(json, run_id)


def _ensure_category_exists(
    category_repository: CategoryRepository,
    settings: Settings,
    category_id: str,
    *,
    is_leaf: bool = True,
) -> None:
    if category_repository.exists(category_id):
        return

    category = _category_from_id(settings, category_id, is_leaf=is_leaf)
    if category.parent_id is not None:
        _ensure_category_exists(
            category_repository,
            settings,
            category.parent_id,
            is_leaf=False,
        )

    category_repository.upsert(category)


def _category_from_id(
    settings: Settings,
    category_id: str,
    *,
    is_leaf: bool,
) -> CategoryNode:
    source_prefix = f"{settings.source_site.value}:"
    if category_id.startswith(source_prefix):
        path = category_id.removeprefix(source_prefix)
    else:
        path = category_id

    path_parts = path.split("/")
    name = path_parts[-1]
    parent_id = None
    if len(path_parts) > 1:
        parent_id = f"{settings.source_site.value}:{path_parts[0]}"

    now = datetime.now()
    return CategoryNode(
        id=category_id,
        source_site=settings.source_site,
        source_category_code=path,
        name=name,
        url=OXILABS_URL_CATEGORY_PREFIX + path,
        path=path,
        parent_id=parent_id,
        level=len(path_parts),
        is_leaf=is_leaf,
        created_at=now,
        updated_at=now,
    )
