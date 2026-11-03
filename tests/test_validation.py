
from services.data_loader import load_leads

from services.validation_service import (
    validate_leads,
    validate_email,
    validate_phone,
)


def test_dataset_has_25_leads():
    df = load_leads()
    assert len(df) == 25


def test_email_validation():
    assert validate_email("test@example.com")
    assert not validate_email("invalid-email")


def test_phone_validation():
    assert validate_phone("01711200101")
    assert not validate_phone("12345")


def test_duplicate_company_detection():
    df = load_leads()
    issues = validate_leads(df)

    duplicate_ids = set(
        issues.loc[
            issues["issue_type"] == "duplicate_company",
            "lead_id"
        ]
    )

    assert {"L01", "L23"}.issubset(duplicate_ids)


def test_date_sequence_detection():
    df = load_leads()
    issues = validate_leads(df)

    invalid_dates = set(
        issues.loc[
            issues["issue_type"] == "invalid_date_sequence",
            "lead_id"
        ]
    )

    assert "L25" in invalid_dates


def test_overdue_followups():
    df = load_leads()
    issues = validate_leads(df)

    overdue_ids = set(
        issues.loc[
            issues["issue_type"] == "overdue_followup",
            "lead_id"
        ]
    )

    assert len(overdue_ids) == 9
