
from database.lead_repository import (
    create_lead,
    get_lead_by_id,
    update_lead,
    delete_lead,
)


def test_create_lead():
    lead = {
        "lead_id": "TEST001",
        "company": "Test Company Ltd",
        "industry": "Technology",
        "contact_name": "Test User",
        "contact_email": "test@example.com",
        "stage": "New",
        "deal_value": 10000,
    }

    # Remove old test record if it exists
    delete_lead("TEST001")

    result = create_lead(lead)

    saved_lead = get_lead_by_id("TEST001")

    assert result["lead_id"] == "TEST001"
    assert saved_lead is not None
    assert saved_lead["company"] == "Test Company Ltd"

    print("CREATE: PASSED")


def test_update_lead():
    lead = get_lead_by_id("TEST001")

    lead["stage"] = "Contacted"
    lead["deal_value"] = 15000

    result = update_lead("TEST001", lead)

    updated_lead = get_lead_by_id("TEST001")

    assert result is True
    assert updated_lead["stage"] == "Contacted"
    assert updated_lead["deal_value"] == 15000

    print("UPDATE: PASSED")


def test_delete_lead():
    result = delete_lead("TEST001")

    deleted_lead = get_lead_by_id("TEST001")

    assert result is True
    assert deleted_lead is None

    print("DELETE: PASSED")


if __name__ == "__main__":
    test_create_lead()
    test_update_lead()
    test_delete_lead()

    print("\nAll Repository CRUD tests passed!")
