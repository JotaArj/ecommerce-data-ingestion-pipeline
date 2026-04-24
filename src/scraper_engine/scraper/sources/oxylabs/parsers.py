from datetime import datetime

from scraper_engine.core.constants import OXILABS_URL_CATEGORY_PREFIX
from scraper_engine.domain.enums import SourceSite
from scraper_engine.domain.models import CategoryNode


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
