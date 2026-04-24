from datetime import datetime
from decimal import Decimal

from playwright.sync_api import Page

from scraper_engine.core.constants import OXILABS_URL_CATEGORY_PREFIX
from scraper_engine.domain.enums import Currency, SourceSite
from scraper_engine.domain.models import (
    CategoryNode,
    Product,
    ProductCategoryLink,
    ProductSnapshot,
)


class Parsers:

    @staticmethod
    def parse_categories(category_urls: list[str]
                         ,subcategory_urls: list[str]
                         ,not_leaf_category_urls: list[str]
    ) -> list[CategoryNode]:
        category_node_list = []

        for category_url in category_urls:
            category_node = CategoryNode (
                id= f"{SourceSite.OXYLABS_SANDBOX.value}:{category_url}",
                source_site=SourceSite.OXYLABS_SANDBOX,
                source_category_code=category_url,
                name=category_url,
                url=OXILABS_URL_CATEGORY_PREFIX + category_url,
                path=category_url,
                parent_id=None,
                level=1,
                is_leaf= category_url not in not_leaf_category_urls,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            category_node_list.append(category_node)
        
        for subcategory_url in subcategory_urls:
            subcategory_url_split = subcategory_url.split("/")
            subcategory = subcategory_url_split[-1]
            parent = subcategory_url_split[0]
            parent_id = f"{SourceSite.OXYLABS_SANDBOX.value}:{parent}"
            category_node = CategoryNode (
                id= f"{SourceSite.OXYLABS_SANDBOX.value}:{subcategory_url}",
                source_site=SourceSite.OXYLABS_SANDBOX,
                source_category_code=subcategory_url,
                name=subcategory,
                url=OXILABS_URL_CATEGORY_PREFIX + subcategory_url,
                path=subcategory_url,
                parent_id=parent_id,
                level=2,
                is_leaf= True,
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            category_node_list.append(category_node)

        return category_node_list
    
    @staticmethod
    def parse_products(page: Page, json: dict[str, object]) -> tuple[list[Product],
                                                               list[ProductSnapshot],
                                                               list[ProductCategoryLink]]:
        products: list[Product] = []
        product_snapshots: list[ProductSnapshot] = []
        product_category_links: list[ProductCategoryLink] = []
        products_json: object = json.get("products")
        if not isinstance(products_json, list):
            return products, product_snapshots, product_category_links

        for data_product in products_json:
            # hacer parseo de todos los campos del producto
            product_name_id = data_product.get("game_name")
            time_at_present = datetime.now()

            title_block = page.locator(
                ".price-wrapper", 
                has=page.locator(".title", has_text="Nintendo Switch"))

            price_text = title_block.locator(".price").inner_text()
            price, currency_symbol = price_text.split(" ")
            


            product = Product(
                id = product_name_id,
                source_site = SourceSite.OXYLABS_SANDBOX,
                source_product_code = data_product.get("id"),
                type = data_product.get("type"),
                name = product_name_id,
                rating = data_product.get("rating"),
                developer = data_product.get("developer"),
                pdp_url = data_product.get("url"),
                created_at = time_at_present,
                updated_at = time_at_present,
                genre = data_product.get("genre") 
                    if isinstance(data_product.get("genre"), list) 
                    else None,
                description = data_product.get("description"),
            )

            products.append(product)

            product_snapshot = ProductSnapshot (
                source_product_id = product_name_id,
                run_id = "0", # sustituir con el run_id
                observed_at = time_at_present,
                current_price = Decimal(price),
                original_price = Decimal(price),
                currency = Parsers._parse_currency(currency_symbol),
                stock_status = data_product.get("inStock"),
                meta_score = data_product.get("inStock"),
                user_score = data_product.get("inStock"),
                created_at = time_at_present
            )

            product_snapshots.append(product_snapshot)

            product_category_link = ProductCategoryLink (
                source_product_id = product_name_id, 
                category_id = data_product.get("platform"),
                created_at = time_at_present
            )

            product_category_links.append(product_category_link)

        return products, product_snapshots, product_category_links

    @staticmethod
    def _parse_currency(currency_symbol: str) -> Currency:
        if currency_symbol == "€":
            return Currency.EUR
        if currency_symbol == "$":
            return Currency.USD
        else:
            return Currency.UNKNOWN
