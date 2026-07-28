from pathlib import Path

# --------------------------------------------------
# Project Paths
# --------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

DATABASE_DIR = BASE_DIR / "database"
LOG_DIR = BASE_DIR / "logs"

DATABASE_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# --------------------------------------------------
# Database
# --------------------------------------------------
DATABASE_NAME = "etf.db"
DATABASE_PATH = DATABASE_DIR / DATABASE_NAME

# --------------------------------------------------
# Logging
# --------------------------------------------------
LOG_FILE = LOG_DIR / "platform.log"
LOG_LEVEL = "INFO"

# --------------------------------------------------
# Application
# --------------------------------------------------
APP_NAME = "GPT Quant Platform"
VERSION = "1.0.0"

# --------------------------------------------------
# Data Collection
# --------------------------------------------------
UPDATE_INTERVAL = 60
DEFAULT_MARKET = "KR"

# --------------------------------------------------
# Score Settings
# --------------------------------------------------
MIN_RETURN_3M = 0.15