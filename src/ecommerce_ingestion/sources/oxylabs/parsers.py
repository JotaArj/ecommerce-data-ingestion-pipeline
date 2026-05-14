import ast
import re
from datetime import datetime
from decimal import Decimal, InvalidOperation

from playwright.sync_api import Page

from ecommerce_ingestion.config.constants import OXILABS_URL_CATEGORY_PREFIX
from ecommerce_ingestion.domain.enums import Currency, SourceSite, StockStatus
from ecommerce_ingestion.domain.models import (
    CategoryNode,
    GameGenre,
    GameGenreLink,
    GameProduct,
    GameProductCategoryLink,
    GameProductSnapshot,
)
from ecommerce_ingestion.sources.oxylabs.selectors import PRICE_SELECTOR


class Parsers:
    PLATFORM_CATEGORY_PATHS = {
        "3ds": "nintendo/3ds",
        "dreamcast": "dreamcast",
        "ds": "nintendo/ds",
        "game-boy-advance": "nintendo/game-boy-advance",
        "game boy advance": "nintendo/game-boy-advance",
        "gamecube": "nintendo/gamecube",
        "nintendo": "nintendo",
        "nintendo 3ds": "nintendo/3ds",
        "nintendo ds": "nintendo/ds",
        "nintendo game boy advance": "nintendo/game-boy-advance",
        "nintendo gamecube": "nintendo/gamecube",
        "nintendo-64": "nintendo/nintendo-64",
        "nintendo switch": "nintendo/switch",
        "pc": "pc",
        "playstation": "playstation-platform",
        "playstation-1": "playstation-platform/playstation-1",
        "playstation 2": "playstation-platform/ps2",
        "playstation-2": "playstation-platform/playstation-2",
        "playstation 3": "playstation-platform/ps3",
        "playstation-3": "playstation-platform/playstation-3",
        "playstation 4": "playstation-platform/ps4",
        "playstation-4": "playstation-platform/playstation-4",
        "playstation 5": "playstation-platform/ps5",
        "playstation-5": "playstation-platform/playstation-5",
        "playstation portable": "playstation-platform/psp",
        "playstation-vita": "playstation-platform/playstation-vita",
        "ps2": "playstation-platform/ps2",
        "ps3": "playstation-platform/ps3",
        "ps4": "playstation-platform/ps4",
        "ps5": "playstation-platform/ps5",
        "psp": "playstation-platform/psp",
        "stadia": "stadia",
        "switch": "nintendo/switch",
        "wii": "nintendo/wii",
        "wii u": "nintendo/wii-u",
        "wii-u": "nintendo/wii-u",
        "xbox": "xbox-platform",
        "xbox-360": "xbox-platform/xbox-360",
        "xbox 360": "xbox-platform/xbox-360",
        "xbox-one": "xbox-platform/xbox-one",
        "xbox one": "xbox-platform/xbox-one",
        "xbox-series-x": "xbox-platform/xbox-series-x",
        "xbox series x": "xbox-platform/xbox-series-x",
    }

    @staticmethod
    def parse_categories(
        category_urls: list[str],
        subcategory_urls: list[str],
        not_leaf_category_urls: list[str],
    ) -> list[CategoryNode]:
        category_node_list: list[CategoryNode] = []

        for category_url in category_urls:
            category_node = CategoryNode(
                category_id=category_url,
                category_source_site=SourceSite.OXYLABS_SANDBOX,
                source_category_code=category_url,
                category_name=category_url,
                category_url=OXILABS_URL_CATEGORY_PREFIX + category_url,
                category_path=category_url,
                category_parent_id=None,
                category_level=1,
                category_is_leaf=category_url not in not_leaf_category_urls,
                category_created_at=datetime.now(),
                category_updated_at=datetime.now(),
            )
            category_node_list.append(category_node)

        for subcategory_url in subcategory_urls:
            subcategory_url_split = subcategory_url.split("/")
            subcategory = subcategory_url_split[-1]
            parent = subcategory_url_split[0]
            parent_id = parent
            category_node = CategoryNode(
                category_id=subcategory_url,
                category_source_site=SourceSite.OXYLABS_SANDBOX,
                source_category_code=subcategory_url,
                category_name=subcategory,
                category_url=OXILABS_URL_CATEGORY_PREFIX + subcategory_url,
                category_path=subcategory_url,
                category_parent_id=parent_id,
                category_level=2,
                category_is_leaf=True,
                category_created_at=datetime.now(),
                category_updated_at=datetime.now(),
            )
            category_node_list.append(category_node)

        return category_node_list

    @staticmethod
    def parse_products(
        page: Page, json: dict[str, object], run_id: str
    ) -> tuple[
        list[GameProduct],
        list[GameProductSnapshot],
        list[GameProductCategoryLink],
        list[GameGenre],
        list[GameGenreLink],
    ]:
        game_products: list[GameProduct] = []
        game_product_snapshots: list[GameProductSnapshot] = []
        game_product_category_links: list[GameProductCategoryLink] = []
        game_genres: list[GameGenre] = []
        game_genre_links: list[GameGenreLink] = []

        page_props = json.get("pageProps")
        if not isinstance(page_props, dict):
            return game_products, game_product_snapshots, game_product_category_links, game_genres, game_genre_links  # noqa: E501

        product_list = page_props.get("products")
        if not isinstance(product_list, list):
            return game_products, game_product_snapshots, game_product_category_links, game_genres, game_genre_links  # noqa: E501

        price_texts = page.locator(PRICE_SELECTOR).all_inner_texts()
        for index, data_product in enumerate(product_list):
            if not isinstance(data_product, dict):
                continue

            game_product_id = Parsers._optional_str(data_product.get("game_name"))
            source_game_product_code = Parsers._optional_str(data_product.get("id"))
            pdp_url = Parsers._optional_str(data_product.get("url"))
            if (
                game_product_id is None
                or source_game_product_code is None
                or pdp_url is None
            ):
                continue

            now = datetime.now()
            price_text = price_texts[index] if index < len(price_texts) else ""
            price, currency = Parsers._parse_price_and_currency(price_text)

            game_product = GameProduct(
                game_id=game_product_id,
                game_source_site=SourceSite.OXYLABS_SANDBOX,
                source_game_product_code=source_game_product_code,
                game_product_type=Parsers._optional_str(data_product.get("type")),
                game_name=game_product_id,
                game_rating=Parsers._optional_str(data_product.get("rating")),
                game_developer=Parsers._optional_str(data_product.get("developer")),
                game_pdp_url=pdp_url,
                game_created_at=now,
                game_updated_at=now,
                game_description=Parsers._optional_str(data_product.get("description")),
            )
            game_products.append(game_product)

            game_product_snapshot = GameProductSnapshot(
                game_product_id=game_product_id,
                run_id=run_id,
                observed_at=now,
                current_price=price,
                original_price=price,
                currency=currency,
                stock_status=Parsers._parse_stock_status(data_product.get("inStock")),
                meta_score=Parsers._parse_decimal(data_product.get("meta_score")),
                user_score=Parsers._parse_decimal(data_product.get("user_score")),
                created_at=now,
            )
            game_product_snapshots.append(game_product_snapshot)

            category_ids = Parsers._parse_category_ids(data_product.get("platform"))
            for category_id in category_ids:
                game_product_category_links.append(
                    GameProductCategoryLink(
                        game_product_id=game_product_id,
                        category_id=category_id,
                        created_at=now,
                    )
                )

            genre_list = Parsers._parse_genre(data_product.get("genre"))
            if genre_list is not None:
                for genre_id in genre_list:
                    game_genre_links.append(
                        GameGenreLink(
                            game_id=game_product_id,
                            genre_id=genre_id,
                        )
                    )
                    game_genres.append(GameGenre(genre_id=genre_id))

        return game_products, game_product_snapshots, game_product_category_links, game_genres, game_genre_links  # noqa: E501

    @staticmethod
    def _parse_price_and_currency(price_text: str) -> tuple[Decimal | None, Currency]:
        currency_symbol = "€" if "€" in price_text else "$" if "$" in price_text else ""
        price_match = re.search(r"\d+(?:[.,]\d+)?", price_text)
        if price_match is None:
            return None, Parsers._parse_currency(currency_symbol)

        return (
            Parsers._parse_decimal(price_match.group(0)),
            Parsers._parse_currency(currency_symbol),
        )

    @staticmethod
    def _parse_currency(currency_symbol: str) -> Currency:
        if currency_symbol == "€":
            return Currency.EUR
        if currency_symbol == "$":
            return Currency.USD
        return Currency.UNKNOWN

    @staticmethod
    def _parse_stock_status(stock_status: object) -> StockStatus:
        if stock_status is True:
            return StockStatus.IN_STOCK
        if stock_status is False:
            return StockStatus.OUT_OF_STOCK
        return StockStatus.UNKNOWN

    @staticmethod
    def _parse_decimal(value: object) -> Decimal | None:
        if value is None or isinstance(value, bool):
            return None
        try:
            return Decimal(str(value).replace(",", "."))
        except (InvalidOperation, ValueError):
            return None

    @staticmethod
    def _optional_str(value: object) -> str | None:
        if isinstance(value, str) and value:
            return value
        if isinstance(value, int | float):
            return str(value)
        return None

    @staticmethod
    def _parse_genre(value: object) -> list[str] | None:
        if isinstance(value, str):
            try:
                value = ast.literal_eval(value)
            except (SyntaxError, ValueError):
                value = [value]

        if not isinstance(value, list):
            return None

        genre = [item.strip().lower() for item in value if isinstance(item, str)]
        return genre or None

    @staticmethod
    def _parse_category_ids(platform: object) -> list[str]:
        if not isinstance(platform, str):
            return []

        platform_names = Parsers._parse_platform_names(platform)
        category_ids: list[str] = []
        for platform_name in platform_names:
            category_path = Parsers.PLATFORM_CATEGORY_PATHS.get(
                platform_name.strip().lower()
            )
            if category_path is not None:
                category_ids.append(category_path)

        return category_ids

    @staticmethod
    def _parse_platform_names(platform: str) -> list[str]:
        try:
            value = ast.literal_eval(platform)
        except (SyntaxError, ValueError):
            return [platform]

        if isinstance(value, list):
            return [item for item in value if isinstance(item, str)]
        if isinstance(value, str):
            return [value]
        return []
