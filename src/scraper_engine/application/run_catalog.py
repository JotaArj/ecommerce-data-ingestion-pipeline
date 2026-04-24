from __future__ import annotations

from playwright.sync_api import Page

from scraper_engine.core.settings import Settings
from scraper_engine.domain.enums import SourceSite
from scraper_engine.domain.models import CategoryNode
from scraper_engine.infra.browser.playwright_factory import PlaywrightFactory
from scraper_engine.infra.db.repositories import CategoryRepository
from scraper_engine.infra.db.sqlite import build_database
from scraper_engine.scraper.sources.oxylabs.discovery import Discovery
from scraper_engine.scraper.sources.oxylabs.scraper import Scraper


def run_catalog(settings: Settings) -> None:
    category_nodes = _discover_categories(settings)
    database = build_database(settings)

    with database.session() as connection:
        category_repository = CategoryRepository(connection)
        for category_node in category_nodes:
            category_repository.upsert(category_node)


def _discover_categories(settings: Settings) -> list[CategoryNode]:
    with PlaywrightFactory(settings) as factory:
        with factory.page_session() as page:
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
