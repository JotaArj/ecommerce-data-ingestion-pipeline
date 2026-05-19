from pathlib import Path

from ecommerce_ingestion.domain.enums import SourceSite

GENRE_MAPPER = {
    "role-playing": ("rpg", 1),
    "action rpg": ("rpg", 1),
    "console-style rpg": ("rpg", 1),
    "japanese-style": ("rpg", 1),
    "pc-style rpg": ("rpg", 1),
    "western-style": ("rpg", 1),

    "action": ("action", 2),
    "action adventure": ("action", 2),
    "beat-'em-up": ("action", 2),
    "open-world": ("action", 2),
    "survival": ("action", 2),

    "shooter": ("shooter", 3),
    "first-person": ("shooter", 3),
    "third-person": ("shooter", 3),
    "light gun": ("shooter", 3),
    "shoot-'em-up": ("shooter", 3),

    "adventure": ("adventure", 4),
    "point-and-click": ("adventure", 4),
    "visual novel": ("adventure", 4),
    "hidden object": ("adventure", 4),
    "text": ("adventure", 4),

    "strategy": ("strategy", 5),
    "tactics": ("strategy", 5),
    "tactical": ("strategy", 5),
    "turn-based": ("strategy", 5),
    "real-time": ("strategy", 5),
    "4x": ("strategy", 5),
    "wargame": ("strategy", 5),
    "city building": ("strategy", 5),
    "management": ("strategy", 5),
    "business / tycoon": ("strategy", 5),
    "tycoon": ("strategy", 5),
    "defense": ("strategy", 5),

    "simulation": ("simulation", 6),
    "sim": ("simulation", 6),
    "flight": ("simulation", 6),
    "driving": ("simulation", 6),
    "sandbox": ("simulation", 6),
    "virtual life": ("simulation", 6),
    "breeding/constructing": ("simulation", 6),
    "trainer": ("simulation", 6),
    "exercise / fitness": ("simulation", 6),

    "sports": ("sports", 7),
    "soccer": ("sports", 7),
    "football": ("sports", 7),
    "basketball": ("sports", 7),
    "tennis": ("sports", 7),
    "golf": ("sports", 7),
    "baseball": ("sports", 7),
    "ice hockey": ("sports", 7),
    "cricket": ("sports", 7),
    "boxing": ("sports", 7),
    "boxing / martial arts": ("sports", 7),
    "wrestling": ("sports", 7),
    "skateboarding": ("sports", 7),
    "skate / skateboard": ("sports", 7),
    "skiing": ("sports", 7),
    "ski / snowboard": ("sports", 7),
    "snowboarding": ("sports", 7),
    "surfing": ("sports", 7),
    "fishing": ("sports", 7),
    "olympic sports": ("sports", 7),
    "athletics": ("sports", 7),
    "volleyball": ("sports", 7),

    "racing": ("racing", 8),
    "kart": ("racing", 8),
    "formula one": ("racing", 8),
    "stock car": ("racing", 8),
    "rally / offroad": ("racing", 8),
    "gt / street": ("racing", 8),
    "motocross": ("racing", 8),

    "puzzle": ("puzzle", 9),
    "logic": ("puzzle", 9),
    "matching": ("puzzle", 9),
    "stacking": ("puzzle", 9),

    "fighting": ("fighting", 10),
    "platformer": ("platformer", 11),

    "music": ("music", 12),
    "rhythm": ("music", 12),
    "dancing": ("music", 12),
    "music maker": ("music", 12),

    "party": ("party", 13),
    "party / minigame": ("party", 13),
    "trivia / game show": ("party", 13),

    "board games": ("board_game", 14),
    "board / card game": ("board_game", 14),
    "card battle": ("board_game", 14),
    "billiards": ("board_game", 14),
    "gambling": ("board_game", 14),
    "parlor": ("board_game", 14),

    "massively multiplayer": ("mmo", 15),
    "massively multiplayer online": ("mmo", 15),
    "moba": ("mmo", 15),

    "arcade": ("arcade", 16),
    "pinball": ("arcade", 16),

    "horror": ("horror", 17),

    "general": ("unknown", 999),
    "miscellaneous": ("unknown", 999),
    "other": ("unknown", 999),
    "": ("unknown", 999),
}

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

DEFAULT_UNKNOWN_RATIO_THRESHOLD = 0.5

CRITICAL_COLUMNS = ["game_id", 
    "game_name", 
    "category_id", 
    "current_price", 
    "stock_status"]

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"
BRONZE_DIR = DATA_DIR / "raw"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
LOGS_DIR = DATA_DIR / "logs"

BRONZE_DATABASE_FILENAME = "oxylabs_sandbox_scraper.db"

SILVER_PRODUCTS_FILENAME = "silver_cleaned_data.parquet"
SILVER_TABLE_EXPORTS: dict[str, str] = {
    "game_genre_game_link": "silver_game_genre_relationships.parquet",
    "game_product_snapshots": "silver_snapshots.parquet",
    "game_genre": "silver_game_genre.parquet"
}

GOLD_TABLE_IMPORTS: dict[str, str] = SILVER_TABLE_EXPORTS | {
    "game_products" : SILVER_PRODUCTS_FILENAME
}

SOURCE_BASE_URLS: dict[SourceSite, str] = {
    SourceSite.OXYLABS_SANDBOX: "https://sandbox.oxylabs.io/products",
    SourceSite.WEBSCRAPER_ECOMMERCE_AJAX: (
        "https://webscraper.io/test-sites/e-commerce/ajax"
    ),
}

DEFAULT_SOURCE_SITE = SourceSite.OXYLABS_SANDBOX
DEFAULT_BASE_URL = SOURCE_BASE_URLS[SourceSite.OXYLABS_SANDBOX]

DEFAULT_HEADLESS = True
DEFAULT_LOG_LEVEL = "INFO"

OXYLABS_CATEGORY_START_PATH = "/products/category/"
OXYLABS_CATEGORY_URL_PREFIX = "https://oxylabs.io/products/category/"

DEFAULT_SCRAPING_URL = "https://sandbox.oxylabs.io/products?page="

# Backward-compatible aliases for notebooks and older imports.
DB_OUTPUT_DIR = DATA_DIR
DB_OUTPUT_BRONZE = BRONZE_DIR
DB_OUTPUT_SILVER = SILVER_DIR
DB_OUTPUT_GOLD = GOLD_DIR
OXYLABS_URL_CATEGORY_PREFIX = OXYLABS_CATEGORY_URL_PREFIX
DEFAULT_SCRAP_URL = DEFAULT_SCRAPING_URL

REGEX_ALPHANUM = r"[^a-zA-Z0-9]+"
