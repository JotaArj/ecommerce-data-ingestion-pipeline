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

        for href in self._get_hrefs(DROPDOWN_MENU_CATEGORIES):
            if href:
                not_leaf_category = href.split(OXYLABS_CATEGORY_START_PATH)[-1]
                not_leaf_category_urls.append(not_leaf_category)

        for href in self._get_hrefs(CATEGORY_LINKS)[1:]:
            if href:
                url_category = href.split(OXYLABS_CATEGORY_START_PATH)[-1]
                url_subcategory = url_category.split("/")
                if len(url_subcategory) > 1:
                    subcategory_urls.append(url_category)
                else:
                    category_urls.append(url_category)

        return Parsers.parse_categories(
            category_urls,
            subcategory_urls,
            not_leaf_category_urls,
        )

    def _get_hrefs(self, selector: str) -> list[str]:
        hrefs: object = self._page.locator(selector).evaluate_all(
            "(elements) => elements.map((element) => "
            "element.getAttribute('href')).filter(Boolean)"
        )
        if not isinstance(hrefs, list):
            return []

        return [href for href in hrefs if isinstance(href, str)]
