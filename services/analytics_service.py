
from database.connection import get_connection
from datetime import date, timedelta


def get_lead_overview():
    """Return overall CRM statistics."""

    query = """
        SELECT
            COUNT(*) AS total_leads,
            COALESCE(SUM(deal_value), 0) AS total_deal_value,
            COUNT(DISTINCT company) AS unique_companies,
            COUNT(DISTINCT industry) AS total_industries
        FROM leads
    """

    with get_connection() as connection:
        row = connection.execute(query).fetchone()

    return dict(row)


def get_stage_distribution():
    """Return lead count and deal value by stage."""

    query = """
        SELECT
            stage,
            COUNT(*) AS total_leads,
            COALESCE(SUM(deal_value), 0) AS total_deal_value
        FROM leads
        GROUP BY stage
        ORDER BY total_leads DESC
    """

    with get_connection() as connection:
        rows = connection.execute(query).fetchall()

    return [dict(row) for row in rows]


def get_industry_distribution():
    """Return lead count by industry."""

    query = """
        SELECT
            COALESCE(NULLIF(industry, ''), 'Unknown') AS industry,
            COUNT(*) AS total_leads,
            COALESCE(SUM(deal_value), 0) AS total_deal_value
        FROM leads
        GROUP BY industry
        ORDER BY total_leads DESC
    """

    with get_connection() as connection:
        rows = connection.execute(query).fetchall()

    return [dict(row) for row in rows]


def get_followup_summary(reference_date=None):
    """Return overdue, today and upcoming follow-ups."""

    if reference_date is None:
        reference_date = date.today()

    reference_date = reference_date.isoformat()
    upcoming_date = (
        date.fromisoformat(reference_date) + timedelta(days=7)
    ).isoformat()

    query = """
        SELECT
            COUNT(
                CASE
                    WHEN next_followup < ? 
                    AND stage NOT IN ('Paid', 'Lost')
                    THEN 1
                END
            ) AS overdue_followups,

            COUNT(
                CASE
                    WHEN next_followup = ?
                    AND stage NOT IN ('Paid', 'Lost')
                    THEN 1
                END
            ) AS due_today,

            COUNT(
                CASE
                    WHEN next_followup > ?
                    AND next_followup <= ?
                    AND stage NOT IN ('Paid', 'Lost')
                    THEN 1
                END
            ) AS upcoming_followups

        FROM leads
        WHERE next_followup IS NOT NULL
          AND next_followup != ''
    """

    with get_connection() as connection:
        row = connection.execute(
            query,
            (
                reference_date,
                reference_date,
                reference_date,
                upcoming_date,
            ),
        ).fetchone()

    return dict(row)


def get_overdue_leads(reference_date=None):
    """Return individual overdue leads."""

    if reference_date is None:
        reference_date = date.today()

    query = """
        SELECT *
        FROM leads
        WHERE next_followup < ?
          AND next_followup IS NOT NULL
          AND next_followup != ''
          AND stage NOT IN ('Paid', 'Lost')
        ORDER BY next_followup ASC
    """

    with get_connection() as connection:
        rows = connection.execute(
            query,
            (reference_date.isoformat(),),
        ).fetchall()

    return [dict(row) for row in rows]


def get_upcoming_leads(reference_date=None, days=7):
    """Return leads requiring follow-up within the next N days."""

    if reference_date is None:
        reference_date = date.today()

    end_date = reference_date + timedelta(days=days)

    query = """
        SELECT *
        FROM leads
        WHERE next_followup >= ?
          AND next_followup <= ?
          AND next_followup IS NOT NULL
          AND next_followup != ''
          AND stage NOT IN ('Paid', 'Lost')
        ORDER BY next_followup ASC
    """

    with get_connection() as connection:
        rows = connection.execute(
            query,
            (
                reference_date.isoformat(),
                end_date.isoformat(),
            ),
        ).fetchall()

    return [dict(row) for row in rows]
