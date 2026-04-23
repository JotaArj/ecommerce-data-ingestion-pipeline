from __future__ import annotations

from playwright.sync_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    sync_playwright,
)

from scraper_engine.core.settings import Settings


class PlaywrightFactory:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._playwright: Playwright | None = None
        self._browser: Browser | None = None

    def start(self) -> None:
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(
            headless=self._settings.headless
        )

    def new_context(self) -> BrowserContext:
        if self._browser is None:
            raise RuntimeError("Browser not started. Call start() first.")

        return self._browser.new_context()

    def new_page(self) -> tuple[BrowserContext, Page]:
        context = self.new_context()
        page = context.new_page()
        return context, page

    def close(self) -> None:
        if self._browser is not None:
            self._browser.close()
            self._browser = None

        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None