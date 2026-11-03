
from datetime import date

from services.analytics_service import (
    get_lead_overview,
    get_stage_distribution,
    get_industry_distribution,
    get_followup_summary,
    get_overdue_leads,
    get_upcoming_leads,
)


def test_lead_overview():
    result = get_lead_overview()

    assert result["total_leads"] == 25
    assert result["total_deal_value"] == 4220000


def test_stage_distribution():
    result = get_stage_distribution()

    assert len(result) > 0

    total = sum(
        item["total_leads"] for item in result
    )

    assert total == 25


def test_industry_distribution():
    result = get_industry_distribution()

    assert len(result) > 0

    total = sum(
        item["total_leads"] for item in result
    )

    assert total == 25


def test_followup_summary():
    result = get_followup_summary(
        reference_date=date(2026, 11, 1)
    )

    assert result["overdue_followups"] == 9
    assert result["due_today"] >= 0
    assert result["upcoming_followups"] >= 0


def test_overdue_leads():
    result = get_overdue_leads(
        reference_date=date(2026, 11, 1)
    )

    assert len(result) == 9


def test_upcoming_leads():
    result = get_upcoming_leads(
        reference_date=date(2026, 11, 1),
        days=7,
    )

    assert isinstance(result, list)
