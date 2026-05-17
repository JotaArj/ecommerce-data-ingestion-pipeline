

PRODUCT_QUERY_JOINED = """
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
        p.game_id,
        p.game_source_site,
        p.source_game_product_code,
        p.game_name,
        p.game_product_type,
        p.game_rating,
        p.game_pdp_url,
        p.game_developer,
        p.game_description,
        g.genres,
        gpc.category_id, 
        gc.category_source_site, 
        gc.source_category_code, 
        gc.category_name, 
        gc.category_url, 
        gc.category_path, 
        gc.category_parent_id, 
        gc.category_level, 
        gc.category_is_leaf, 
        gpsl.current_price,
        gpsl.currency,
        gpsl.stock_status,
        gpsl.meta_score,
        gpsl.user_score
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
