from playwright.sync_api import Page

from src.sources.oxylabs.selectors import DROPDOWN_MENU_CATEGORIES


class Scraper:
    def __init__(self, page: Page) -> None:
        self._page = page

    def expand_category_menu(self) -> None:
        dropdown_menu_categories = self._page.locator(DROPDOWN_MENU_CATEGORIES)
        count = dropdown_menu_categories.count()

        for i in range(1, count):
            dropdown_menu_categories.nth(i).click()
