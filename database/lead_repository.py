
from database.connection import get_connection


def create_lead(lead_data: dict):
    """Create a new lead in the database."""

    query = """
        INSERT INTO leads (
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

    values = (
        lead_data["lead_id"],
        lead_data["company"],
        lead_data.get("industry"),
        lead_data.get("contact_name"),
        lead_data.get("contact_role"),
        lead_data.get("contact_email"),
        lead_data.get("contact_phone"),
        lead_data.get("source"),
        lead_data.get("stage", "New"),
        lead_data.get("deal_value", 0),
        lead_data.get("last_contact"),
        lead_data.get("next_followup"),
        lead_data.get("notes"),
    )

    with get_connection() as connection:
        connection.execute(query, values)

    return lead_data


def get_all_leads():
    """Retrieve all leads from the database."""

    query = """
        SELECT *
        FROM leads
        ORDER BY created_at DESC
    """

    with get_connection() as connection:
        rows = connection.execute(query).fetchall()

    return [dict(row) for row in rows]


def get_lead_by_id(lead_id: str):
    """Retrieve a single lead using its ID."""

    query = """
        SELECT *
        FROM leads
        WHERE lead_id = ?
    """

    with get_connection() as connection:
        row = connection.execute(
            query, (lead_id,)
        ).fetchone()

    return dict(row) if row else None


def update_lead(lead_id: str, lead_data: dict):
    """Update an existing lead."""

    query = """
        UPDATE leads
        SET
            company = ?,
            industry = ?,
            contact_name = ?,
            contact_role = ?,
            contact_email = ?,
            contact_phone = ?,
            source = ?,
            stage = ?,
            deal_value = ?,
            last_contact = ?,
            next_followup = ?,
            notes = ?,
            updated_at = CURRENT_TIMESTAMP
        WHERE lead_id = ?
    """

    values = (
        lead_data["company"],
        lead_data.get("industry"),
        lead_data.get("contact_name"),
        lead_data.get("contact_role"),
        lead_data.get("contact_email"),
        lead_data.get("contact_phone"),
        lead_data.get("source"),
        lead_data.get("stage", "New"),
        lead_data.get("deal_value", 0),
        lead_data.get("last_contact"),
        lead_data.get("next_followup"),
        lead_data.get("notes"),
        lead_id,
    )

    with get_connection() as connection:
        cursor = connection.execute(query, values)

    return cursor.rowcount > 0


def delete_lead(lead_id: str):
    """Delete a lead using its ID."""

    query = """
        DELETE FROM leads
        WHERE lead_id = ?
    """

    with get_connection() as connection:
        cursor = connection.execute(
            query, (lead_id,)
        )

    return cursor.rowcount > 0
