from __future__ import annotations

from collections.abc import Iterator
from contextlib import contextmanager

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
        if self._playwright is not None or self._browser is not None:
            return

        playwright = sync_playwright().start()
        try:
            browser = playwright.chromium.launch(headless=self._settings.headless)
        except Exception:
            playwright.stop()
            raise

        self._playwright = playwright
        self._browser = browser

    def __enter__(self) -> PlaywrightFactory:
        self.start()
        return self

    def __exit__(self, exc_type: object, exc: object, tb: object) -> None:
        self.close()

    def new_context(self) -> BrowserContext:
        if self._browser is None:
            raise RuntimeError("Browser not started. Call start() first.")

        return self._browser.new_context()

    def new_page(self) -> tuple[BrowserContext, Page]:
        context = self.new_context()
        page = context.new_page()
        return context, page

    @contextmanager
    def page_session(self) -> Iterator[Page]:
        context, page = self.new_page()
        try:
            yield page
        finally:
            context.close()

    def close(self) -> None:
        if self._browser is not None:
            self._browser.close()
            self._browser = None

        if self._playwright is not None:
            self._playwright.stop()
            self._playwright = None
