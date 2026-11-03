
import json

import pytest

from services import ai_service
from services.ai_service import (
    AIServiceError,
    _prepare_business_context,
    ask_business_question,
    generate_business_summary,
)


@pytest.fixture
def sample_leads():
    return [
        {
            "lead_id": "L001",
            "company": "Alpha Technologies",
            "industry": "Technology",
            "stage": "Meeting",
            "deal_value": 500000,
            "source": "Website",
            "last_contact": "2026-10-28",
            "next_followup": "2026-11-05",
            "contact_name": "John Doe",
            "contact_email": "john@example.com",
            "contact_phone": "0123456789",
            "notes": "Confidential customer notes",
        },
        {
            "lead_id": "L002",
            "company": "Beta Solutions",
            "industry": "Finance",
            "stage": "Proposal",
            "deal_value": 300000,
            "source": "Referral",
            "last_contact": "2026-10-29",
            "next_followup": "2026-11-06",
            "contact_name": "Jane Doe",
            "contact_email": "jane@example.com",
            "contact_phone": "01987654321",
            "notes": "Private business information",
        },
    ]


def test_prepare_business_context(sample_leads):
    context = json.loads(_prepare_business_context(sample_leads))

    assert context["total_leads"] == 2
    assert context["total_deal_value_bdt"] == 800000
    assert context["stage_distribution"]["Meeting"] == 1
    assert context["stage_distribution"]["Proposal"] == 1


def test_business_context_excludes_sensitive_fields(sample_leads):
    context = _prepare_business_context(sample_leads)

    assert "contact_name" not in context
    assert "contact_email" not in context
    assert "contact_phone" not in context
    assert "notes" not in context
    assert "john@example.com" not in context
    assert "Confidential customer notes" not in context



def test_empty_leads_rejected():
    with pytest.raises(ValueError, match="No business data available"):
        ask_business_question("Give me a business summary", [])


def test_empty_question_rejected(sample_leads):
    with pytest.raises(ValueError, match="Question cannot be empty"):
        ask_business_question("   ", sample_leads)



def test_gemini_api_failure_handled(sample_leads, monkeypatch):
    class FakeResponse:
        text = None

    class FakeModels:
        def generate_content(self, **kwargs):
            raise RuntimeError("Simulated API failure")

    class FakeClient:
        models = FakeModels()

    monkeypatch.setattr(ai_service, "_get_client", lambda: FakeClient())

    with pytest.raises(AIServiceError):
        ask_business_question("Analyze the leads", sample_leads)


def test_business_summary_uses_ai_service(sample_leads, monkeypatch):
    expected = "Business summary generated successfully"

    monkeypatch.setattr(
        ai_service,
        "ask_business_question",
        lambda question, leads: expected,
    )

    assert generate_business_summary(sample_leads) == expected
