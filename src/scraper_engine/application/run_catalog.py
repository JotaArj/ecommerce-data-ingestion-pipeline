from __future__ import annotations

from playwright.sync_api import Page

from scraper_engine.core.settings import Settings
from scraper_engine.domain.enums import SourceSite
from scraper_engine.domain.models import (
    CategoryNode,
    Product,
    ProductCategoryLink,
    ProductSnapshot,
)
from scraper_engine.infra.browser.playwright_factory import PlaywrightFactory
from scraper_engine.infra.db.repositories import (
    CategoryRepository,
    ProductCategoryRepository,
    ProductRepository,
    ProductSnapshotRepository,
)
from scraper_engine.infra.db.sqlite import build_database
from scraper_engine.scraper.sources.oxylabs.discovery import Discovery
from scraper_engine.scraper.sources.oxylabs.scraper import Scraper


def run_catalog(settings: Settings) -> None:
    with PlaywrightFactory(settings) as factory:
        with factory.page_session() as page:
            database = build_database(settings)
            with database.session() as connection:
                category_repository = CategoryRepository(connection)
                product_category_repository = ProductCategoryRepository(connection)
                product_snapshot_repository = ProductSnapshotRepository(connection)
                product_repository = ProductRepository(connection)

                category_nodes = _discover_categories(settings, page)
                for category_node in category_nodes:
                    category_repository.upsert(category_node)

                json = capture_products_json_from_navigation(settings, page, 1)
                total_pages, products_per_page = _capture_atributes_from_json(json)

                for i in range(total_pages +1):
                    json = capture_products_json_from_navigation(settings, page, i + 1)
                    (
                        products,
                        product_snapshots,
                        product_category_links,
                    ) = _discover_products_from_json(page, json)

                    for product in products:
                        product_repository.upsert(product)

                    for product_snapshot in product_snapshots:
                        product_snapshot_repository.insert(product_snapshot)

                    for product_category_link in product_category_links:
                        product_category_repository.upsert(product_category_link)

                #       guardar productos en base de datos


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
        lambda response: "products.json" in response.url
    ) as response_info:
        page.goto(settings.start_scraping_url + str(num_page), 
                  wait_until="domcontentloaded")

    response = response_info.value
    payload: object = response.json()
    if not isinstance(payload, dict):
        raise ValueError("Expected products JSON response to be an object")

    result: dict[str, object] = {}
    for key, value in payload.items():
        key_object: object = key
        value_object: object = value
        if not isinstance(key_object, str):
            raise ValueError("Expected products JSON response keys to be strings")
        result[key_object] = value_object

    return result


def _capture_atributes_from_json(json: dict[str, object]) -> tuple[int, int]:
    page_props: object = json["pageProps"]
    if not isinstance(page_props, dict):
        raise ValueError("Expected pageProps to be an object")

    page_count: object = page_props["pageCount"]
    per_page: object = page_props["perPage"]
    if not isinstance(page_count, int) or not isinstance(per_page, int):
        raise ValueError("Expected pageCount and perPage to be integers")

    return page_count, per_page

def _discover_products_from_json(page: Page, 
                                 json: dict[str, object]) -> tuple[list[Product], 
                                                                               list[ProductSnapshot], 
                                                                               list[ProductCategoryLink]]:
    discovery = Discovery(page)
    return discovery.discover_products(page, json)