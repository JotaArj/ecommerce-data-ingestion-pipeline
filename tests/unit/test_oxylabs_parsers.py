from __future__ import annotations

from decimal import Decimal

from scraper_engine.domain.enums import Currency
from scraper_engine.scraper.sources.oxylabs.parsers import Parsers
from scraper_engine.scraper.sources.oxylabs.selectors import PRICE_SELECTOR


class _FakeLocator:
    def __init__(self, texts: list[str]) -> None:
        self._texts = texts

    def all_inner_texts(self) -> list[str]:
        return self._texts


class _FakePage:
    def __init__(self, price_texts: list[str]) -> None:
        self._price_texts = price_texts
        self.selectors: list[str] = []

    def locator(self, selector: str) -> _FakeLocator:
        self.selectors.append(selector)
        return _FakeLocator(self._price_texts)


def test_parse_products_reads_price_from_price_wrapper() -> None:
    page = _FakePage(["91,99 €"])
    payload = {
        "pageProps": {
            "products": [
                {
                    "id": 1,
                    "game_name": "The Legend of Zelda: Ocarina of Time",
                    "url": "https://www.metacritic.com/game/nintendo-64/game",
                    "platform": "['nintendo-64']",
                    "genre": "['Action Adventure', 'Fantasy']",
                    "inStock": True,
                }
            ]
        }
    }

    products, snapshots, links = Parsers.parse_products(page, payload, "run-1")

    assert page.selectors == [PRICE_SELECTOR]
    assert products[0].genre == ["Action Adventure", "Fantasy"]
    assert snapshots[0].current_price == Decimal("91.99")
    assert snapshots[0].currency == Currency.EUR
    assert [link.category_id for link in links] == [
        "oxylabs_sandbox:nintendo/nintendo-64"
    ]


def test_parse_category_ids_accepts_game_boy_advance_slug() -> None:
    assert Parsers._parse_category_ids("['game-boy-advance']") == [
        "oxylabs_sandbox:nintendo/game-boy-advance"
    ]
