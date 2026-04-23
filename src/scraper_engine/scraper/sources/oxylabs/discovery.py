from playwright.sync_api import Page

from scraper_engine.core.constants import OXYLABS_CATEGORY_START_PATH
from scraper_engine.domain.models import CategoryNode
from scraper_engine.scraper.sources.oxylabs.parsers import Parsers
from scraper_engine.scraper.sources.oxylabs.selectors import (
    CATEGORY_LINKS,
    DROPDOWN_MENU_CATEGORIES,
)


class Discovery:

    def __init__(self, page: Page) -> None: 
        self._page = page

# The first category is discarded due to being all products.
    def discover_categories(self) -> list[CategoryNode]:

        not_leaf_category_urls = []
        category_urls = []
        subcategory_urls = []
        
        dropdown_category = self._page.locator(DROPDOWN_MENU_CATEGORIES)
        dropdown_category_count = dropdown_category.count()

        for i in range(dropdown_category_count):
            href = dropdown_category.nth(i).get_attribute("href")
            if href:
                not_leaf_category = href.split(OXYLABS_CATEGORY_START_PATH)[-1]
                not_leaf_category_urls.append(not_leaf_category)
        
        category_links = self._page.locator(CATEGORY_LINKS)  # noqa: E501
        category_count = category_links.count()

        for i in range(1, category_count):
            href = category_links.nth(i).get_attribute("href")
            if href:
                url_category = href.split(OXYLABS_CATEGORY_START_PATH)[-1]
                url_subcategory = url_category.split("/")
                if len(url_subcategory) > 1:
                    subcategory_urls.append(url_category)
                else:
                    category_urls.append(url_category)

        return Parsers.parse_categories(category_urls, 
                                        subcategory_urls, 
                                        not_leaf_category_urls)      