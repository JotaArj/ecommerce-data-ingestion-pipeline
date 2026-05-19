from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

DATA_DIR = PROJECT_ROOT / "data"
BRONZE_DIR = DATA_DIR / "raw"
SILVER_DIR = DATA_DIR / "silver"
GOLD_DIR = DATA_DIR / "gold"
LOGS_DIR = DATA_DIR / "logs"

BRONZE_DATABASE_FILENAME = "oxylabs_sandbox_scraper.db"

# Backward-compatible aliases for notebooks and older exploration code.
DB_OUTPUT_DIR = DATA_DIR
DB_OUTPUT_BRONZE = BRONZE_DIR
DB_OUTPUT_SILVER = SILVER_DIR
DB_OUTPUT_GOLD = GOLD_DIR
