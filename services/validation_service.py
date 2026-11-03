
import re
from datetime import date

import pandas as pd


REFERENCE_DATE = date(2026, 11, 1)


def normalize_text(value):
    """Normalize text for comparison."""
    if pd.isna(value):
        return ""

    return str(value).strip().lower()


def validate_email(email):
    """Check basic email syntax."""

    if pd.isna(email) or not str(email).strip():
        return False

    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"

    return bool(re.match(pattern, str(email).strip()))


def validate_phone(phone):
    """Validate Bangladeshi mobile number format."""

    if pd.isna(phone) or not str(phone).strip():
        return False

    digits = re.sub(r"\D", "", str(phone))

    return bool(
        re.fullmatch(r"01[3-9]\d{8}", digits)
        or re.fullmatch(r"8801[3-9]\d{8}", digits)
    )


def validate_leads(df):
    """
    Validate corporate leads and generate
    a structured data quality report.
    """

    issues = []

    def add_issue(lead_id, issue_type, severity,
                  description, recommendation):

        issues.append({
            "lead_id": lead_id,
            "issue_type": issue_type,
            "severity": severity,
            "description": description,
            "recommendation": recommendation,
        })

    data = df.copy()

    # Parse dates without modifying original data
    data["_last_contact"] = pd.to_datetime(
        data["last contact"], errors="coerce"
    )

    data["_next_followup"] = pd.to_datetime(
        data["next follow-up"], errors="coerce"
    )

    # 1. Missing information
    required_fields = [
        "contact name",
        "contact role",
        "contact email",
        "contact phone",
    ]

    for _, row in data.iterrows():

        lead_id = row["lead id"]

        for field in required_fields:

            if normalize_text(row[field]) == "":
                add_issue(
                    lead_id,
                    "missing_information",
                    "High",
                    f"Missing {field}.",
                    f"Provide a valid {field}."
                )

    # 2. Email validation
    for _, row in data.iterrows():

        email = row["contact email"]

        if normalize_text(email) and not validate_email(email):
            add_issue(
                row["lead id"],
                "invalid_email",
                "High",
                f"Invalid email format: {email}",
                "Verify and correct the email address."
            )
    
    
    # 2B. Email review signals from supplied notes
    for _, row in data.iterrows():

        notes = normalize_text(row["notes"])

        if "typo" in notes or "check before sending" in notes:
            add_issue(
                row["lead id"],
                "email_manual_review",
                "Medium",
                "Lead notes indicate a possible email typo.",
                "Verify the email address with the contact."
            )


    # 3. Phone validation
    for _, row in data.iterrows():

        phone = row["contact phone"]

        if normalize_text(phone) and not validate_phone(phone):
            add_issue(
                row["lead id"],
                "invalid_phone",
                "Medium",
                f"Invalid phone number: {phone}",
                "Verify the Bangladeshi mobile number."
            )

    # 4. Duplicate company detection
    company_groups = data.groupby(
        data["company"].apply(normalize_text)
    )

    for company, group in company_groups:

        if company and len(group) > 1:

            lead_ids = group["lead id"].tolist()

            for lead_id in lead_ids:
                add_issue(
                    lead_id,
                    "duplicate_company",
                    "High",
                    f"Potential duplicate company: {company}. "
                    f"Related leads: {lead_ids}",
                    "Review the company records before merging."
                )

    # 5. Duplicate contact detection using email
    data["_normalized_email"] = (
        data["contact email"]
        .apply(normalize_text)
    )

    email_groups = data[
        data["_normalized_email"] != ""
    ].groupby("_normalized_email")

    for email, group in email_groups:

        if len(group) > 1:

            lead_ids = group["lead id"].tolist()

            for lead_id in lead_ids:
                add_issue(
                    lead_id,
                    "duplicate_contact",
                    "High",
                    f"Contact email appears in multiple leads: {email}. "
                    f"Related leads: {lead_ids}",
                    "Review whether these records represent "
                    "the same contact."
                )

    # 6. Missing date detection
    for _, row in data.iterrows():

        lead_id = row["lead id"]

        if pd.isna(row["_last_contact"]):
            add_issue(
                lead_id,
                "missing_last_contact",
                "Medium",
                "Last contact date is missing or invalid.",
                "Record the last contact date if known."
            )

        if pd.isna(row["_next_followup"]):
            add_issue(
                lead_id,
                "missing_followup",
                "High",
                "Next follow-up date is missing or invalid.",
                "Schedule the next follow-up date."
            )

    # 7. Date sequence validation
    for _, row in data.iterrows():

        last_contact = row["_last_contact"]
        next_followup = row["_next_followup"]

        if (
            pd.notna(last_contact)
            and pd.notna(next_followup)
            and next_followup < last_contact
        ):
            add_issue(
                row["lead id"],
                "invalid_date_sequence",
                "High",
                "Next follow-up is before last contact.",
                "Correct the follow-up date."
            )

    # 8. Overdue follow-up detection
    for _, row in data.iterrows():

        followup = row["_next_followup"]

        if (
            pd.notna(followup)
            and followup.date() < REFERENCE_DATE
        ):
            add_issue(
                row["lead id"],
                "overdue_followup",
                "Medium",
                f"Follow-up date {followup.date()} "
                f"is before {REFERENCE_DATE}.",
                "Review the lead and update its follow-up."
            )

    return pd.DataFrame(issues)


def generate_quality_summary(issues):

    if issues.empty:
        return {
            "total_issues": 0,
            "affected_leads": 0,
            "high_severity": 0,
            "medium_severity": 0,
        }

    return {
        "total_issues": len(issues),
        "affected_leads": issues["lead_id"].nunique(),
        "high_severity": int(
            (issues["severity"] == "High").sum()
        ),
        "medium_severity": int(
            (issues["severity"] == "Medium").sum()
        ),
    }
