
from pathlib import Path

import pandas as pd


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Official sample dataset
DATA_PATH = BASE_DIR / "data" / "raw" / "corporate-leads.csv"


EXPECTED_COLUMNS = [
    "lead id",
    "company",
    "industry",
    "contact name",
    "contact role",
    "contact email",
    "contact phone",
    "source",
    "stage",
    "deal value (BDT)",
    "last contact",
    "next follow-up",
    "notes",
]


def load_leads() -> pd.DataFrame:
    """
    Load the original BIAI corporate leads dataset.
    """

    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"Dataset not found: {DATA_PATH}"
        )

    df = pd.read_csv(DATA_PATH, encoding="utf-8-sig")

    missing_columns = set(EXPECTED_COLUMNS) - set(df.columns)

    if missing_columns:
        raise ValueError(
            f"Missing required columns: {missing_columns}"
        )

    return df
