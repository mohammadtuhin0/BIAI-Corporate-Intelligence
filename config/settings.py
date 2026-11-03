
import os
from pathlib import Path

from dotenv import load_dotenv


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables
load_dotenv(BASE_DIR / ".env")

# Gemini configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "").strip()

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.8-flash"
).strip()

# Database configuration
DATABASE_PATH = Path(
    os.getenv(
        "DATABASE_PATH",
        "data/biai_crm.db"
    )
)

if not DATABASE_PATH.is_absolute():
    DATABASE_PATH = BASE_DIR / DATABASE_PATH


def is_gemini_configured():
    """Check whether Gemini API credentials are configured."""

    return bool(
        GEMINI_API_KEY
        and GEMINI_API_KEY != "YOUR_ACTUAL_API_KEY"
        and GEMINI_MODEL
    )
