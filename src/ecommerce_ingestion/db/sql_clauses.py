from ecommerce_ingestion.config.silver_config import SILVER_PRODUCT_SELECT_COLUMNS

PRODUCT_QUERY_JOINED = f"""
    WITH genre_links_grouped AS (
    SELECT
        game_id,
        GROUP_CONCAT(genre_id, ', ') AS genres
    FROM game_genre_game_link
    GROUP BY game_id
    ),
    game_product_snapshots_latest AS (
        SELECT
            *
        FROM game_product_snapshots AS gps
        WHERE observed_at = (
            SELECT MAX(g2.observed_at)
            FROM game_product_snapshots AS g2
            WHERE g2.game_product_id = gps.game_product_id
        )
    )
    SELECT
       {", ".join(SILVER_PRODUCT_SELECT_COLUMNS)}
    FROM game_products AS p
    LEFT JOIN genre_links_grouped AS g
        ON p.game_id = g.game_id
    LEFT JOIN game_product_categories AS gpc
        ON p.game_id = gpc.game_product_id
    LEFT JOIN category_nodes AS gc
        ON gpc.category_id = gc.category_id
    LEFT JOIN game_product_snapshots_latest AS gpsl
        ON p.game_id = gpsl.game_product_id;
"""
