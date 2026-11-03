
import pytest

from services.lead_service import (
    create_new_lead,
    list_leads,
    find_lead,
    update_existing_lead,
    remove_lead,
)


def test_list_leads():
    leads = list_leads()
    assert len(leads) == 25


def test_find_lead():
    lead = find_lead("L01")
    assert lead is not None
    assert lead["company"] == "Padma Textiles Ltd"


def test_create_lead_validation():
    with pytest.raises(ValueError):
        create_new_lead({
            "lead_id": "INVALID001",
            "company": "Invalid Company",
            "stage": "Unknown Stage",
        })


def test_negative_deal_value():
    with pytest.raises(ValueError):
        create_new_lead({
            "lead_id": "INVALID002",
            "company": "Invalid Company",
            "deal_value": -500,
        })


def test_find_nonexistent_lead():
    assert find_lead("NOT_FOUND") is None
