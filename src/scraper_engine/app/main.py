from __future__ import annotations

from scraper_engine.core.settings import load_settings
from scraper_engine.infra.browser.playwright_factory import PlaywrightFactory


def main() -> None:
    settings = load_settings()
    factory = PlaywrightFactory(settings)

    factory.start()

    context, page = factory.new_page()
    try:
        page.goto(settings.base_url, wait_until="domcontentloaded")
        print(page.title())
        print(page.url)
    finally:
        context.close()
        factory.close()


if __name__ == "__main__":
    main()
