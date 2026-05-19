import logging
from datetime import datetime
from math import ceil
from uuid import uuid4

from playwright.sync_api import Page

from ecommerce_ingestion.browser.playwright_factory import PlaywrightFactory
from ecommerce_ingestion.config.logging_config import configure_logging
from ecommerce_ingestion.config.settings import ScraperSettings, load_scrapper_settings
from ecommerce_ingestion.config.source_config import OXYLABS_URL_CATEGORY_PREFIX
from ecommerce_ingestion.db.init_db import initialize_database_if_missing
from ecommerce_ingestion.db.repositories import (
    CategoryRepository,
    GameGenreGameLinkRepository,
    GameGenreRepository,
    GameProductCategoryRepository,
    GameProductRepository,
    GameProductSnapshotRepository,
    RunRepository,
)
from ecommerce_ingestion.db.sqlite import SQLiteDatabase, build_database
from ecommerce_ingestion.domain.enums import RunStatus, RunType, SourceSite
from ecommerce_ingestion.domain.models import (
    CategoryNode,
    GameGenre,
    GameGenreLink,
    GameProduct,
    GameProductCategoryLink,
    GameProductSnapshot,
    ScraperRun,
)
from ecommerce_ingestion.sources.oxylabs.discovery import Discovery
from ecommerce_ingestion.sources.oxylabs.scraper import Scraper
from ecommerce_ingestion.sources.oxylabs.selectors import PRICE_SELECTOR

logger = logging.getLogger(__name__)

def run_catalog(source_site: SourceSite, run_name: str | None = None) -> None:
    settings = load_scrapper_settings(source_site, run_name)
    initialize_database_if_missing(settings)
    configure_logging(settings)
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
                    game_product_category_repository = GameProductCategoryRepository(
                        connection
                    )
                    game_product_snapshot_repository = GameProductSnapshotRepository(
                        connection
                    )
                    game_product_repository = GameProductRepository(connection)
                    game_genre_repository = GameGenreRepository(connection)
                    game_genre_game_link_repository = GameGenreGameLinkRepository(connection)  # noqa: E501

                    category_nodes = _discover_categories(settings, page)
                    logger.info("Discovered %s categories", len(category_nodes))
                    for category_node in category_nodes:
                        category_repository.upsert(category_node)

                    products_payload = capture_products_payload_from_navigation(
                        settings, page, 1
                    )
                    total_pages, products_per_page = (
                        _capture_attributes_from_payload(products_payload)
                    )
                    logger.info(
                        "Catalog has %s pages with %s products per page",
                        total_pages,
                        products_per_page,
                    )

                    for page_number in range(1, total_pages + 1):
                        products_payload = capture_products_payload_from_navigation(
                            settings, page, page_number
                        )
                        (
                            game_products,
                            game_product_snapshots,
                            game_product_category_links,
                            game_genres,
                            game_genre_links,
                        ) = _discover_products_from_payload(
                            page, run.id, products_payload
                        )

                        for game_product in game_products:
                            game_product_repository.upsert(game_product)

                        for game_product_category_link in game_product_category_links:
                            _ensure_category_exists(
                                category_repository,
                                settings,
                                game_product_category_link.category_id,
                            )
                            game_product_category_repository.upsert(
                                game_product_category_link
                            )

                        for game_product_snapshot in game_product_snapshots:
                            game_product_snapshot_repository.insert(
                                game_product_snapshot
                            )

                        for game_genre in game_genres:
                            game_genre_repository.upsert(game_genre)

                        for game_genre_link in game_genre_links:
                            game_genre_game_link_repository.upsert(game_genre_link)

                        total_products += len(game_products)
                        total_snapshots += len(game_product_snapshots)
                        total_links += len(game_product_category_links)

                        logger.info(
                            "Processed page %s: "
                            "%s products, "
                            "%s snapshots, "
                            "%s category links",
                            page_number,
                            len(game_products),
                            len(game_product_snapshots),
                            len(game_product_category_links),
                        )

        run.status = RunStatus.SUCCEEDED
        run.finished_at = datetime.now()
        _save_run(database, run)
        logger.info(
            "Catalog run %s succeeded: "
            "%s products, "
            "%s snapshots, "
            "%s category links, ",
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

def _save_run(database: SQLiteDatabase, run: ScraperRun) -> None:
    with database.session() as connection:
        RunRepository(connection).upsert(run)


def _discover_categories(settings: ScraperSettings, page: Page) -> list[CategoryNode]:
    page.goto(settings.base_url, wait_until="domcontentloaded")
    return _discover_categories_for_source(page, settings)


def _discover_categories_for_source(
    page: Page, settings: ScraperSettings
) -> list[CategoryNode]:
    if settings.source_site is SourceSite.OXYLABS_SANDBOX:
        scraper = Scraper(page)
        scraper.expand_category_menu()

        discovery = Discovery(page)
        return discovery.discover_categories()

    raise NotImplementedError(
        f"Catalog runner not implemented for source site: {settings.source_site}"
    )


def capture_products_payload_from_navigation(
    settings: ScraperSettings, page: Page, num_page: int
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


def _capture_attributes_from_payload(payload: dict[str, object]) -> tuple[int, int]:
    page_props: object = payload["pageProps"]
    if not isinstance(page_props, dict):
        raise ValueError("Expected pageProps to be an object")

    page_count: object = page_props["pageCount"]
    per_page: object = page_props["perPage"]
    if not isinstance(page_count, int) or not isinstance(per_page, int):
        raise ValueError("Expected pageCount and perPage to be integers")

    return page_count, per_page


def _discover_products_from_payload(
    page: Page, run_id: str, payload: dict[str, object]
) -> tuple[
    list[GameProduct],
    list[GameProductSnapshot],
    list[GameProductCategoryLink],
    list[GameGenre],
    list[GameGenreLink],
]:
    discovery = Discovery(page)

    return discovery.discover_products(payload, run_id)


def _ensure_category_exists(
    category_repository: CategoryRepository,
    settings: ScraperSettings,
    category_id: str,
    *,
    is_leaf: bool = True,
) -> None:
    if category_repository.exists(category_id):
        return

    category = _category_from_id(settings, category_id, is_leaf=is_leaf)
    if category.category_parent_id is not None:
        _ensure_category_exists(
            category_repository,
            settings,
            category.category_parent_id,
            is_leaf=False,
        )

    category_repository.upsert(category)


def _category_from_id(
    settings: ScraperSettings,
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
    category_name = path_parts[-1]
    parent_id = None
    if len(path_parts) > 1:
        parent_id = path_parts[0]

    now = datetime.now()
    return CategoryNode(
        category_id=category_id,
        category_source_site=settings.source_site,
        source_category_code=path,
        category_name=category_name,
        category_url=OXYLABS_URL_CATEGORY_PREFIX + path,
        category_path=path,
        category_parent_id=parent_id,
        category_level=len(path_parts),
        category_is_leaf=is_leaf,
        category_created_at=now,
        category_updated_at=now,
    )
