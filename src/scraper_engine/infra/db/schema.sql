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

CREATE TABLE IF NOT EXISTS products (
    id TEXT PRIMARY KEY,
    source_site TEXT NOT NULL,
    source_product_code TEXT NOT NULL,
    name TEXT NOT NULL,
    product_type TEXT,
    rating TEXT,
    pdp_url TEXT NOT NULL,
    developer TEXT,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    genre TEXT,
    description TEXT,
    UNIQUE (source_site, source_product_code),
    UNIQUE (source_site, pdp_url)
);

CREATE TABLE IF NOT EXISTS categories (
    id TEXT PRIMARY KEY,
    source_site TEXT NOT NULL,
    source_category_code TEXT NOT NULL,
    name TEXT NOT NULL,
    url TEXT NOT NULL,
    path TEXT NOT NULL,
    parent_id TEXT,
    level INTEGER NOT NULL,
    is_leaf INTEGER NOT NULL,
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL,
    FOREIGN KEY (parent_id) REFERENCES categories(id),
    UNIQUE (source_site, source_category_code),
    UNIQUE (source_site, url)
);

CREATE TABLE IF NOT EXISTS product_categories (
    source_product_id TEXT NOT NULL,
    category_id TEXT NOT NULL,
    created_at TEXT NOT NULL,
    PRIMARY KEY (source_product_id, category_id),
    FOREIGN KEY (source_product_id) REFERENCES products(id),
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS product_snapshots (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source_product_id TEXT NOT NULL,
    run_id TEXT NOT NULL,
    observed_at TEXT NOT NULL,
    current_price NUMERIC,
    original_price NUMERIC,
    currency TEXT NOT NULL,
    stock_status TEXT NOT NULL,
    meta_score NUMERIC,
    user_score NUMERIC,
    created_at TEXT NOT NULL,
    FOREIGN KEY (source_product_id) REFERENCES products(id),
    FOREIGN KEY (run_id) REFERENCES runs(id)
);

CREATE INDEX IF NOT EXISTS idx_runs_source_site
    ON runs(source_site);

CREATE INDEX IF NOT EXISTS idx_products_source_site
    ON products(source_site);

CREATE INDEX IF NOT EXISTS idx_categories_source_site
    ON categories(source_site);

CREATE INDEX IF NOT EXISTS idx_categories_parent_id
    ON categories(parent_id);

CREATE INDEX IF NOT EXISTS idx_product_categories_category_id
    ON product_categories(category_id);

CREATE INDEX IF NOT EXISTS idx_product_snapshots_source_product_id
    ON product_snapshots(source_product_id);

CREATE INDEX IF NOT EXISTS idx_product_snapshots_run_id
    ON product_snapshots(run_id);

CREATE INDEX IF NOT EXISTS idx_product_snapshots_observed_at
    ON product_snapshots(observed_at);
