
import os
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent.parent

# Local development: load .env
load_dotenv(BASE_DIR / ".env")


def get_setting(name, default=""):
    """Read Streamlit Cloud secrets first, then environment variables."""
    try:
        value = st.secrets.get(name, None)
    except Exception:
        value = None

    if value is None:
        value = os.getenv(name, default)

    return str(value).strip()


# Gemini configuration
GEMINI_API_KEY = get_setting("GEMINI_API_KEY")
GEMINI_MODEL = get_setting("GEMINI_MODEL", "gemini-3.6-flash")

# Database configuration
DATABASE_PATH = Path(
    get_setting("DATABASE_PATH", "data/biai_crm.db")
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

