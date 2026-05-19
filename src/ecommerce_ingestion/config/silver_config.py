SILVER_SELECT_COLUMNS = [
    "p.game_id",
    "p.game_source_site",
    "p.source_game_product_code",
    "p.game_name",
    "p.game_product_type",
    "p.game_rating",
    "p.game_pdp_url",
    "p.game_developer",
    "p.game_description",
    "g.genres",
    "gpc.category_id",
    "gc.category_source_site",
    "gc.source_category_code",
    "gc.category_name",
    "gc.category_url",
    "gc.category_path",
    "gc.category_parent_id",
    "gc.category_level",
    "gc.category_is_leaf",
    "gpsl.current_price",
    "gpsl.currency",
    "gpsl.stock_status",
    "gpsl.meta_score",
    "gpsl.user_score",
]

SILVER_COLUMNS_REQUIRED = [
    "game_id",
    "game_source_site",
    "source_game_product_code",
    "game_name",
    "game_product_type",
    "game_rating",
    "game_pdp_url",
    "game_developer",
    "game_description",
    "genres",
    "category_id",
    "category_source_site",
    "source_category_code",
    "category_name",
    "category_url",
    "category_path",
    "category_parent_id",
    "category_level",
    "category_is_leaf",
    "current_price",
    "currency",
    "stock_status",
    "meta_score",
    "user_score",
]

CRITICAL_COLUMNS = [
    "game_id",
    "game_name",
    "category_id",
    "current_price",
    "stock_status",
]

DEFAULT_UNKNOWN_RATIO_THRESHOLD = 0.5

SILVER_PRODUCTS_FILENAME = "silver_cleaned_data.parquet"
SILVER_TABLE_EXPORTS: dict[str, str] = {
    "game_genre_game_link": "silver_game_genre_relationships.parquet",
    "game_product_snapshots": "silver_snapshots.parquet",
    "game_genre": "silver_game_genre.parquet",
}
