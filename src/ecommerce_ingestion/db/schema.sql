PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS runs (
    id TEXT PRIMARY KEY,
    run_type TEXT NOT NULL,
    source_site TEXT NOT NULL,
    status TEXT NOT NULL,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS game_products (
    game_id TEXT PRIMARY KEY,
    game_source_site TEXT NOT NULL,
    source_game_product_code TEXT NOT NULL,
    game_name TEXT NOT NULL,
    game_product_type TEXT,
    game_rating TEXT,
    game_pdp_url TEXT NOT NULL,
    game_developer TEXT,
    game_created_at TEXT NOT NULL,
    game_updated_at TEXT NOT NULL,
    game_description TEXT
);

CREATE TABLE IF NOT EXISTS category_nodes (
    category_id TEXT PRIMARY KEY,
    category_source_site TEXT NOT NULL,
    source_category_code TEXT NOT NULL,
    category_name TEXT NOT NULL,
    category_url TEXT NOT NULL,
    category_path TEXT NOT NULL,
    category_parent_id TEXT,
    category_level INTEGER NOT NULL,
    category_is_leaf INTEGER NOT NULL,
    category_created_at TEXT NOT NULL,
    category_updated_at TEXT NOT NULL,
    FOREIGN KEY (category_parent_id) REFERENCES category_nodes(category_id),
    UNIQUE (category_source_site, source_category_code),
    UNIQUE (category_source_site, category_url)
);

CREATE TABLE IF NOT EXISTS game_product_categories (
    game_product_id TEXT NOT NULL,
    category_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (game_product_id, category_id),
    FOREIGN KEY (game_product_id) REFERENCES game_products(game_id),
    FOREIGN KEY (category_id) REFERENCES category_nodes(category_id)
);

CREATE TABLE IF NOT EXISTS game_product_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    game_product_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    current_price NUMERIC,
    original_price NUMERIC,
    currency TEXT NOT NULL,
    stock_status TEXT NOT NULL,
    meta_score NUMERIC,
    user_score NUMERIC,
    created_at TEXT NOT NULL,
    FOREIGN KEY (game_product_id) REFERENCES game_products(game_id),
    FOREIGN KEY (run_id) REFERENCES runs(id)
);

CREATE TABLE IF NOT EXISTS game_genre (
    genre_id TEXT PRIMARY KEY UNIQUE
);

CREATE TABLE IF NOT EXISTS game_genre_game_link (
    game_id TEXT NOT NULL,
    genre_id TEXT NOT NULL,
    PRIMARY KEY (game_id, genre_id),
    FOREIGN KEY (game_id) REFERENCES game_products(game_id),
    FOREIGN KEY (genre_id) REFERENCES game_genre(genre_id)
);

CREATE INDEX IF NOT EXISTS idx_runs_source_site
    ON runs(source_site);

CREATE INDEX IF NOT EXISTS idx_game_products_source_site
    ON game_products(game_source_site);

CREATE INDEX IF NOT EXISTS idx_category_nodes_source_site
    ON category_nodes(category_source_site);

CREATE INDEX IF NOT EXISTS idx_category_nodes_parent_id
    ON category_nodes(category_parent_id);

CREATE INDEX IF NOT EXISTS idx_game_product_categories_category_id
    ON game_product_categories(category_id);

CREATE INDEX IF NOT EXISTS idx_game_product_snapshots_game_product_id
    ON game_product_snapshots(game_product_id);

CREATE INDEX IF NOT EXISTS idx_game_product_snapshots_run_id
    ON game_product_snapshots(run_id);

CREATE INDEX IF NOT EXISTS idx_game_product_snapshots_observed_at
    ON game_product_snapshots(observed_at);

CREATE INDEX IF NOT EXISTS idx_game_product_snapshots_game_product_observed_at
    ON game_product_snapshots(game_product_id, observed_at);

CREATE INDEX IF NOT EXISTS idx_game_genre_game_link_genre_id
    ON game_genre_game_link(genre_id);

