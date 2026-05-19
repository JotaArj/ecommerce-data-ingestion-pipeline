from __future__ import annotations

from decimal import Decimal
from typing import cast

from playwright.sync_api import Page

from ecommerce_ingestion.domain.enums import Currency
from ecommerce_ingestion.sources.oxylabs.parsers import Parsers
from ecommerce_ingestion.sources.oxylabs.selectors import PRICE_SELECTOR


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
    payload: dict[str, object] = {
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

    game_products, snapshots, links, genres, genre_links = Parsers.parse_products(
        cast(Page, page), payload, "run-1"
    )

    assert page.selectors == [PRICE_SELECTOR]
    assert [genre.genre_id for genre in genres] == ["action adventure", "fantasy"]
    assert [link.genre_id for link in genre_links] == ["action adventure", "fantasy"]
    assert game_products[0].game_id == (
        "the legend of zelda: ocarina of time::nintendo/nintendo-64"
    )
    assert game_products[0].game_name == "The Legend of Zelda: Ocarina of Time"
    assert snapshots[0].game_product_id == game_products[0].game_id
    assert genre_links[0].game_id == game_products[0].game_id
    assert snapshots[0].current_price == Decimal("91.99")
    assert snapshots[0].currency == Currency.EUR
    assert [link.category_id for link in links] == ["nintendo/nintendo-64"]
    assert links[0].game_product_id == game_products[0].game_id


def test_parse_category_ids_accepts_game_boy_advance_slug() -> None:
    assert Parsers._parse_category_ids("['game-boy-advance']") == [
        "nintendo/game-boy-advance"
    ]


def test_parse_products_creates_one_product_per_category() -> None:
    page = _FakePage(["19.99 $"])
    payload: dict[str, object] = {
        "pageProps": {
            "products": [
                {
                    "id": 10,
                    "game_name": "Shared Game",
                    "url": "https://www.metacritic.com/game/shared-game",
                    "platform": "['switch', 'ps5']",
                    "genre": "['Action']",
                    "inStock": True,
                }
            ]
        }
    }

    game_products, snapshots, links, _genres, genre_links = Parsers.parse_products(
        cast(Page, page), payload, "run-1"
    )

    assert [product.game_id for product in game_products] == [
        "shared game::nintendo/switch",
        "shared game::playstation-platform/ps5",
    ]
    assert [snapshot.game_product_id for snapshot in snapshots] == [
        "shared game::nintendo/switch",
        "shared game::playstation-platform/ps5",
    ]
    assert [link.category_id for link in links] == [
        "nintendo/switch",
        "playstation-platform/ps5",
    ]
    assert [link.game_id for link in genre_links] == [
        "shared game::nintendo/switch",
        "shared game::playstation-platform/ps5",
    ]
