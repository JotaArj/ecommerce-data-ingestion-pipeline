NamedAggregation = tuple[str, str]
GoldAggregationConfig = dict[str, NamedAggregation | tuple[str, object]]

PERFORMANCE_AGGREGATIONS: GoldAggregationConfig = {
    "game_count": ("game_id", "count"),
    "average_user_score": ("user_score", "mean"),
    "average_meta_score": ("meta_score", "mean"),
    "average_price": ("current_price", "mean"),
    "in_stock_percentage": (
        "stock_status",
        lambda values: (values == "in_stock").mean() * 100,
    ),
}

PLATFORM_PERFORMANCE_GROUP_COLUMNS = ["category_name"]
GENRE_PERFORMANCE_GROUP_COLUMNS = ["unified_genre"]
PRICE_DISTRIBUTION_GROUP_COLUMNS = [
    "price_bucket",
    "category_name",
    "unified_genre",
]
