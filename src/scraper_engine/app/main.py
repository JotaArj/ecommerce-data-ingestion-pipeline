from __future__ import annotations

from pprint import pprint

from scraper_engine.core.settings import load_settings
from scraper_engine.infra.browser.playwright_factory import PlaywrightFactory
from scraper_engine.scraper.sources.oxylabs.discovery import Discovery
from scraper_engine.scraper.sources.oxylabs.scraper import Scraper


def main() -> None:
    settings = load_settings()
    factory = PlaywrightFactory(settings)

    factory.start()

    context, page = factory.new_page()
    try:
        page.goto(settings.base_url, wait_until="domcontentloaded")
        scraper = Scraper(page)
        scraper.expand_category_menu()

        discovery = Discovery(page)
        category_node_list = discovery.discover_categories()  # noqa: E501

        pprint(category_node_list)
        print(len(category_node_list))

        
    finally:
        context.close()
        factory.close()


if __name__ == "__main__":
    main()
