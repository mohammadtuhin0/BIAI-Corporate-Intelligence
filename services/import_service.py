
from services.data_loader import load_leads
from database.connection import get_connection
import pandas as pd


def _clean(value):
    """Convert missing values to None and clean text values."""
    if pd.isna(value):
        return None

    value = str(value).strip()
    return value if value else None


def import_leads():
    """
    Import corporate leads from CSV into SQLite.
    Existing lead IDs will be ignored to prevent duplicates.
    """

    df = load_leads()

    records = []

    for _, row in df.iterrows():
        deal_value = pd.to_numeric(
            row["deal value (BDT)"],
            errors="coerce"
        )

        records.append((
            _clean(row["lead id"]),
            _clean(row["company"]),
            _clean(row["industry"]),
            _clean(row["contact name"]),
            _clean(row["contact role"]),
            _clean(row["contact email"]),
            _clean(row["contact phone"]),
            _clean(row["source"]),
            _clean(row["stage"]),
            0.0 if pd.isna(deal_value) else float(deal_value),
            _clean(row["last contact"]),
            _clean(row["next follow-up"]),
            _clean(row["notes"]),
        ))

    query = """
        INSERT OR IGNORE INTO leads (
            lead_id,
            company,
            industry,
            contact_name,
            contact_role,
            contact_email,
            contact_phone,
            source,
            stage,
            deal_value,
            last_contact,
            next_followup,
            notes
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    with get_connection() as connection:

        before_count = connection.execute(
            "SELECT COUNT(*) FROM leads"
        ).fetchone()[0]

        connection.executemany(query, records)

        after_count = connection.execute(
            "SELECT COUNT(*) FROM leads"
        ).fetchone()[0]

    inserted = after_count - before_count
    skipped = len(records) - inserted

    return {
        "total_csv_records": len(records),
        "inserted": inserted,
        "skipped": skipped,
        "total_database_records": after_count,
    }
