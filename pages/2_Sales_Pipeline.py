
import streamlit as st
import pandas as pd
import plotly.express as px

from services.lead_service import list_leads


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Sales Pipeline | BIAI",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Pipeline")
st.caption("Track leads, monitor sales stages, and analyze deal values.")

st.divider()


# --------------------------------------------------
# Load Leads
# --------------------------------------------------

try:
    leads = list_leads()

    if not leads:
        st.info("No leads available. Please add leads first.")
        st.stop()

    df = pd.DataFrame(leads)

except Exception as error:
    st.error(f"Unable to load leads: {error}")
    st.stop()


# --------------------------------------------------
# Stage Configuration
# --------------------------------------------------

STAGE_ORDER = [
    "New",
    "Contacted",
    "Meeting",
    "Proposal",
    "Invoice sent",
    "Paid",
    "Lost"
]

df["deal_value"] = pd.to_numeric(
    df["deal_value"], errors="coerce"
).fillna(0)


# --------------------------------------------------
# Filters
# --------------------------------------------------

st.subheader("Filter Pipeline")

col1, col2 = st.columns(2)

with col1:
    selected_stages = st.multiselect(
        "Select Sales Stages",
        options=STAGE_ORDER,
        default=STAGE_ORDER
    )

with col2:
    industries = sorted(
        df["industry"].dropna().unique().tolist()
    )

    selected_industries = st.multiselect(
        "Select Industries",
        options=industries,
        default=industries
    )

filtered_df = df[
    df["stage"].isin(selected_stages)
    & df["industry"].isin(selected_industries)
].copy()

st.divider()


# --------------------------------------------------
# Pipeline Summary
# --------------------------------------------------

st.subheader("Pipeline Overview")

total_leads = len(filtered_df)
total_deal_value = filtered_df["deal_value"].sum()

active_leads = filtered_df[
    ~filtered_df["stage"].isin(["Paid", "Lost"])
]

active_pipeline_value = active_leads["deal_value"].sum()

paid_leads = filtered_df[
    filtered_df["stage"] == "Paid"
]

paid_value = paid_leads["deal_value"].sum()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Leads", total_leads)

col2.metric(
    "Total Deal Value",
    f"৳{total_deal_value:,.0f}"
)

col3.metric(
    "Active Pipeline Value",
    f"৳{active_pipeline_value:,.0f}"
)

col4.metric(
    "Paid Deal Value",
    f"৳{paid_value:,.0f}"
)

st.divider()


# --------------------------------------------------
# Stage-wise Lead Distribution
# --------------------------------------------------

st.subheader("Sales Stage Distribution")

stage_summary = (
    filtered_df.groupby("stage")
    .agg(
        total_leads=("lead_id", "count"),
        deal_value=("deal_value", "sum")
    )
    .reindex(STAGE_ORDER, fill_value=0)
    .reset_index()
    .rename(columns={"index": "stage"})
)

col1, col2 = st.columns(2)

with col1:
    fig = px.funnel(
        stage_summary,
        x="total_leads",
        y="stage",
        title="Lead Distribution Across Stages",
        labels={
            "total_leads": "Number of Leads",
            "stage": "Sales Stage"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

with col2:
    fig = px.bar(
        stage_summary,
        x="stage",
        y="deal_value",
        title="Deal Value by Sales Stage",
        labels={
            "stage": "Sales Stage",
            "deal_value": "Deal Value (BDT)"
        },
        text_auto=".2s"
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()


# --------------------------------------------------
# Industry-wise Pipeline
# --------------------------------------------------

st.subheader("Industry-wise Pipeline")

industry_summary = (
    filtered_df.groupby("industry")
    .agg(
        total_leads=("lead_id", "count"),
        total_deal_value=("deal_value", "sum")
    )
    .reset_index()
    .sort_values("total_deal_value", ascending=False)
)

if not industry_summary.empty:
    fig = px.bar(
        industry_summary,
        x="industry",
        y="total_deal_value",
        color="industry",
        title="Deal Value by Industry",
        labels={
            "industry": "Industry",
            "total_deal_value": "Deal Value (BDT)"
        }
    )

    st.plotly_chart(fig, use_container_width=True)

st.divider()


# --------------------------------------------------
# Lead Pipeline Table
# --------------------------------------------------

st.subheader("Lead Pipeline Details")

display_columns = [
    "lead_id",
    "company",
    "industry",
    "stage",
    "deal_value",
    "contact_name",
    "next_followup"
]

available_columns = [
    column for column in display_columns
    if column in filtered_df.columns
]

st.dataframe(
    filtered_df[available_columns],
    use_container_width=True,
    hide_index=True
)

st.caption(
    f"Showing {len(filtered_df)} leads from the selected filters."
)
