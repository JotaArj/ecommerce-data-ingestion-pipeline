

from playwright.sync_api import Page

from scraper_engine.scraper.sources.oxylabs.selectors import DROPDOWN_MENU_CATEGORIES


class Scraper:

    def __init__(self, page: Page) -> None:
        self._page = page

# All dropdown menu has the attribute a with href containing "/products/category/", 
# the first one is opened by default  # noqa: E501
    def expand_category_menu(self) -> None:
            dropdown_menu_categories = self._page.locator(DROPDOWN_MENU_CATEGORIES)
            count = dropdown_menu_categories.count()

            for i in range(1, count):
                dropdown_menu_categories.nth(i).click()
