
import streamlit as st
import pandas as pd
import plotly.express as px

from services.lead_service import list_leads
from services.validation_service import (
    validate_leads,
    generate_quality_summary,
    REFERENCE_DATE,
)


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Data Quality | BIAI",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 Data Quality Dashboard")

st.caption(
    "Monitor data accuracy, identify errors, "
    "and improve corporate lead quality."
)

st.divider()


# --------------------------------------------------
# Load Database Records
# --------------------------------------------------

try:
    leads = list_leads()

    if not leads:
        st.info("No lead records available.")
        st.stop()

    db_df = pd.DataFrame(leads)

except Exception as error:
    st.error(f"Unable to load lead records: {error}")
    st.stop()


# --------------------------------------------------
# Map Database Columns to Validation Columns
# --------------------------------------------------

column_mapping = {
    "lead_id": "lead id",
    "contact_name": "contact name",
    "contact_role": "contact role",
    "contact_email": "contact email",
    "contact_phone": "contact phone",
    "last_contact": "last contact",
    "next_followup": "next follow-up",
}

validation_df = db_df.rename(
    columns=column_mapping
)


# --------------------------------------------------
# Run Validation Engine
# --------------------------------------------------

issues = validate_leads(validation_df)

summary = generate_quality_summary(issues)

total_leads = len(db_df)

affected_leads = summary["affected_leads"]

clean_leads = total_leads - affected_leads

quality_percentage = (
    (clean_leads / total_leads) * 100
    if total_leads else 0
)


# --------------------------------------------------
# Overview Metrics
# --------------------------------------------------

st.subheader("Data Quality Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Leads",
    total_leads
)

col2.metric(
    "Total Issues",
    summary["total_issues"]
)

col3.metric(
    "Affected Leads",
    affected_leads
)

col4.metric(
    "Data Quality Score",
    f"{quality_percentage:.1f}%"
)

st.caption(
    "Data Quality Score = Leads without detected issues "
    "/ Total Leads. It is a record-level indicator, "
    "not a field-level accuracy measurement."
)

st.divider()


# --------------------------------------------------
# Severity Overview
# --------------------------------------------------

st.subheader("Issue Severity")

col1, col2, col3 = st.columns(3)

col1.metric(
    "High Severity",
    summary["high_severity"]
)

col2.metric(
    "Medium Severity",
    summary["medium_severity"]
)

col3.metric(
    "Low Severity",
    0
)

st.divider()


# --------------------------------------------------
# Issue Type Analysis
# --------------------------------------------------

st.subheader("Issue Type Analysis")

if not issues.empty:

    issue_summary = (
        issues.groupby("issue_type")
        .size()
        .reset_index(name="count")
        .sort_values("count", ascending=False)
    )

    col1, col2 = st.columns(2)

    with col1:

        fig = px.bar(
            issue_summary,
            x="issue_type",
            y="count",
            color="count",
            title="Issues by Type",
            labels={
                "issue_type": "Issue Type",
                "count": "Number of Issues"
            }
        )

        fig.update_layout(
            xaxis_tickangle=-35
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

    with col2:

        severity_data = (
            issues.groupby("severity")
            .size()
            .reset_index(name="count")
        )

        fig = px.pie(
            severity_data,
            names="severity",
            values="count",
            title="Severity Distribution",
            hole=0.4
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

else:

    st.success("No data quality issues detected.")

st.divider()


# --------------------------------------------------
# Issue Filters
# --------------------------------------------------

st.subheader("Data Quality Issue Report")

if not issues.empty:

    col1, col2 = st.columns(2)

    with col1:

        severity_options = sorted(
            issues["severity"].unique().tolist()
        )

        selected_severities = st.multiselect(
            "Filter by Severity",
            options=severity_options,
            default=severity_options
        )

    with col2:

        issue_options = sorted(
            issues["issue_type"].unique().tolist()
        )

        selected_issue_types = st.multiselect(
            "Filter by Issue Type",
            options=issue_options,
            default=issue_options
        )

    filtered_issues = issues[
        issues["severity"].isin(selected_severities)
        & issues["issue_type"].isin(selected_issue_types)
    ].copy()

    search_query = st.text_input(
        "Search by Lead ID or Description"
    )

    if search_query.strip():

        search_query = search_query.strip().lower()

        filtered_issues = filtered_issues[
            filtered_issues["lead_id"]
            .astype(str)
            .str.lower()
            .str.contains(search_query, na=False)
            |
            filtered_issues["description"]
            .astype(str)
            .str.lower()
            .str.contains(search_query, na=False)
        ]

    st.caption(
        f"Showing {len(filtered_issues)} issues."
    )

    st.dataframe(
        filtered_issues,
        use_container_width=True,
        hide_index=True
    )

    # Download filtered report

    csv_data = filtered_issues.to_csv(
        index=False
    ).encode("utf-8-sig")

    st.download_button(
        label="📥 Download Quality Report (CSV)",
        data=csv_data,
        file_name="biai_data_quality_report.csv",
        mime="text/csv"
    )

else:

    st.success("There are no issues to display.")

st.divider()


# --------------------------------------------------
# Affected Lead Records
# --------------------------------------------------

st.subheader("Affected Lead Records")

if not issues.empty:

    affected_ids = issues["lead_id"].unique()

    affected_records = db_df[
        db_df["lead_id"].isin(affected_ids)
    ].copy()

    affected_records["issue_count"] = (
        affected_records["lead_id"]
        .map(issues.groupby("lead_id").size())
    )

    affected_records = affected_records.sort_values(
        "issue_count",
        ascending=False
    )

    st.dataframe(
        affected_records[
            [
                "lead_id",
                "company",
                "contact_email",
                "contact_phone",
                "stage",
                "issue_count"
            ]
        ],
        use_container_width=True,
        hide_index=True
    )

else:

    st.success("All lead records passed validation.")

st.divider()


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption(
    f"BIAI Corporate Intelligence | "
    f"Validation reference date: {REFERENCE_DATE}"
)
