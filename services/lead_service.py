
from database.lead_repository import (
    create_lead,
    get_all_leads,
    get_lead_by_id,
    update_lead,
    delete_lead,
)


VALID_STAGES = [
    "New",
    "Contacted",
    "Meeting",
    "Proposal",
    "Invoice sent",
    "Paid",
    "Lost",
]


def create_new_lead(lead_data: dict):
    """Validate and create a new lead."""

    required_fields = ["lead_id", "company"]

    for field in required_fields:
        if not lead_data.get(field):
            raise ValueError(f"{field} is required.")

    stage = lead_data.get("stage", "New")

    if stage not in VALID_STAGES:
        raise ValueError("Invalid lead stage.")

    deal_value = lead_data.get("deal_value", 0)

    try:
        deal_value = float(deal_value)
    except (TypeError, ValueError):
        raise ValueError("Deal value must be numeric.")

    if deal_value < 0:
        raise ValueError("Deal value cannot be negative.")

    lead_data = lead_data.copy()
    lead_data["stage"] = stage
    lead_data["deal_value"] = deal_value

    return create_lead(lead_data)


def list_leads():
    """Return all leads."""

    return get_all_leads()


def find_lead(lead_id: str):
    """Find a lead by ID."""

    if not lead_id or not lead_id.strip():
        raise ValueError("Lead ID is required.")

    return get_lead_by_id(lead_id.strip())


def update_existing_lead(lead_id: str, lead_data: dict):
    """Validate and update an existing lead."""

    existing_lead = find_lead(lead_id)

    if existing_lead is None:
        raise ValueError("Lead not found.")

    if not lead_data.get("company"):
        raise ValueError("Company name is required.")

    stage = lead_data.get("stage", existing_lead["stage"])

    if stage not in VALID_STAGES:
        raise ValueError("Invalid lead stage.")

    deal_value = lead_data.get(
        "deal_value",
        existing_lead["deal_value"]
    )

    try:
        deal_value = float(deal_value)
    except (TypeError, ValueError):
        raise ValueError("Deal value must be numeric.")

    if deal_value < 0:
        raise ValueError("Deal value cannot be negative.")

    updated_data = existing_lead.copy()
    updated_data.update(lead_data)
    updated_data["stage"] = stage
    updated_data["deal_value"] = deal_value

    return update_lead(lead_id, updated_data)


def remove_lead(lead_id: str):
    """Delete an existing lead."""

    existing_lead = find_lead(lead_id)

    if existing_lead is None:
        raise ValueError("Lead not found.")

    return delete_lead(lead_id)
