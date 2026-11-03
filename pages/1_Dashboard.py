
import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date

from services.analytics_service import (
    get_lead_overview,
    get_stage_distribution,
    get_industry_distribution,
    get_followup_summary,
    get_overdue_leads,
    get_upcoming_leads,
)


# --------------------------------------------------
# Page Configuration
# --------------------------------------------------

st.set_page_config(
    page_title="Dashboard | BIAI CRM",
    page_icon="📊",
    layout="wide",
)


# --------------------------------------------------
# Dashboard Header
# --------------------------------------------------

st.title("📊 Corporate Intelligence Dashboard")

st.caption(
    "Real-time sales pipeline analytics and corporate lead insights."
)

st.write(f"Report Date: **{date.today().strftime('%d %B %Y')}**")

st.divider()


# --------------------------------------------------
# Load Analytics Data
# --------------------------------------------------

try:
    overview = get_lead_overview()
    stage_data = get_stage_distribution()
    industry_data = get_industry_distribution()

    followup_summary = get_followup_summary()

    overdue_leads = get_overdue_leads()
    upcoming_leads = get_upcoming_leads()

except Exception as error:
    st.error(f"Unable to load dashboard data: {error}")
    st.stop()


# --------------------------------------------------
# KPI Metrics
# --------------------------------------------------

st.subheader("Business Overview")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric(
        "Total Leads",
        f"{overview['total_leads']:,}",
    )

with col2:
    st.metric(
        "Total Deal Value",
        f"৳{overview['total_deal_value']:,.0f}",
    )

with col3:
    st.metric(
        "Unique Companies",
        f"{overview['unique_companies']:,}",
    )

with col4:
    st.metric(
        "Industries",
        f"{overview['total_industries']:,}",
    )

with col5:
    st.metric(
        "Overdue Follow-ups",
        f"{followup_summary['overdue_followups']:,}",
    )


st.divider()


# --------------------------------------------------
# Follow-up Summary
# --------------------------------------------------

st.subheader("📅 Follow-up Overview")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Overdue",
        followup_summary["overdue_followups"],
    )

with col2:
    st.metric(
        "Due Today",
        followup_summary["due_today"],
    )

with col3:
    st.metric(
        "Upcoming (7 Days)",
        followup_summary["upcoming_followups"],
    )


st.divider()


# --------------------------------------------------
# Prepare DataFrames
# --------------------------------------------------

stage_df = pd.DataFrame(stage_data)
industry_df = pd.DataFrame(industry_data)

overdue_df = pd.DataFrame(overdue_leads)
upcoming_df = pd.DataFrame(upcoming_leads)


# --------------------------------------------------
# Stage Distribution Chart
# --------------------------------------------------

st.subheader("Sales Pipeline Analysis")

col1, col2 = st.columns(2)

with col1:

    st.markdown("**Lead Distribution by Stage**")

    if not stage_df.empty:

        fig_stage = px.bar(
            stage_df,
            x="stage",
            y="total_leads",
            color="stage",
            text="total_leads",
            labels={
                "stage": "Sales Stage",
                "total_leads": "Number of Leads",
            },
            title="Corporate Leads by Stage",
        )

        fig_stage.update_layout(
            showlegend=False,
            xaxis_title="Stage",
            yaxis_title="Total Leads",
        )

        st.plotly_chart(
            fig_stage,
            use_container_width=True,
        )

    else:
        st.info("No stage data available.")


# --------------------------------------------------
# Industry Distribution Chart
# --------------------------------------------------

with col2:

    st.markdown("**Industry Distribution**")

    if not industry_df.empty:

        fig_industry = px.pie(
            industry_df,
            names="industry",
            values="total_leads",
            hole=0.45,
            title="Leads by Industry",
        )

        fig_industry.update_traces(
            textposition="inside",
            textinfo="percent+label",
        )

        st.plotly_chart(
            fig_industry,
            use_container_width=True,
        )

    else:
        st.info("No industry data available.")


st.divider()


# --------------------------------------------------
# Deal Value by Stage
# --------------------------------------------------

st.subheader("💰 Deal Value Analysis")

if not stage_df.empty:

    fig_deal = px.bar(
        stage_df.sort_values("total_deal_value"),
        x="total_deal_value",
        y="stage",
        orientation="h",
        text="total_deal_value",
        color="stage",
        labels={
            "stage": "Sales Stage",
            "total_deal_value": "Deal Value (BDT)",
        },
        title="Deal Value by Sales Stage",
    )

    fig_deal.update_layout(
        showlegend=False,
        xaxis_title="Deal Value (BDT)",
        yaxis_title="Sales Stage",
    )

    fig_deal.update_traces(
        texttemplate="৳%{x:,.0f}",
        textposition="outside",
    )

    st.plotly_chart(
        fig_deal,
        use_container_width=True,
    )

else:
    st.info("No deal value data available.")


st.divider()


# --------------------------------------------------
# Overdue Follow-up Table
# --------------------------------------------------

st.subheader("⚠️ Overdue Follow-ups")

if not overdue_df.empty:

    overdue_columns = [
        "lead_id",
        "company",
        "contact_name",
        "contact_email",
        "stage",
        "next_followup",
    ]

    st.dataframe(
        overdue_df[overdue_columns],
        use_container_width=True,
        hide_index=True,
    )

else:
    st.success("No overdue follow-ups!")


st.divider()


# --------------------------------------------------
# Upcoming Follow-up Table
# --------------------------------------------------

st.subheader("🔔 Upcoming Follow-ups")

if not upcoming_df.empty:

    upcoming_columns = [
        "lead_id",
        "company",
        "contact_name",
        "contact_email",
        "stage",
        "next_followup",
    ]

    st.dataframe(
        upcoming_df[upcoming_columns],
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info("No upcoming follow-ups in the next 7 days.")


st.divider()


# --------------------------------------------------
# Footer
# --------------------------------------------------

st.caption(
    "BIAI Corporate Intelligence | AI Sales CRM | "
    "Powered by Python, Streamlit, SQLite and Plotly"
)
