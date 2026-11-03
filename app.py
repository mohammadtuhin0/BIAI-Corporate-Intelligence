
import streamlit as st

from services.lead_service import list_leads


from database.connection import initialize_database
from services.import_service import import_leads


@st.cache_resource
def bootstrap_database():
    """Initialize database and import the CSV on first app startup."""
    initialize_database()
    return import_leads()


try:
    import_result = bootstrap_database()
except Exception as error:
    st.error(f"Database initialization failed: {error}")
    st.stop()


st.set_page_config(
    page_title="BIAI Corporate Intelligence",
    page_icon="📊",
    layout="wide",
)

st.title("📊 BIAI Corporate Intelligence")
st.subheader("AI-Powered Corporate CRM & Business Intelligence")

st.markdown(
    """
    Welcome to BIAI Corporate Intelligence.

    Manage corporate leads, monitor sales performance,
    maintain data quality, and generate AI-powered
    business insights from one platform.
    """
)

try:
    leads = list_leads()

    total_leads = len(leads)
    total_value = sum(
        float(lead.get("deal_value") or 0)
        for lead in leads
    )

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Total Corporate Leads", total_leads)

    with col2:
        st.metric("Total Deal Value", f"৳{total_value:,.0f}")

except Exception as error:
    st.error(f"Unable to load CRM data: {error}")

st.divider()

st.subheader("🚀 Platform Modules")

col1, col2 = st.columns(2)

with col1:
    st.markdown(
        """
        **📈 Dashboard & Analytics**

        Monitor lead performance and business metrics.

        **👥 Lead Management**

        Create, update, search, and manage corporate leads.

        **📊 Sales Pipeline**

        Track sales stages and deal values.
        """
    )

with col2:
    st.markdown(
        """
        **🔍 Data Quality**

        Detect missing information, invalid data,
        duplicates, and overdue follow-ups.

        **🤖 AI Business Assistant**

        Generate business summaries, lead insights,
        and follow-up recommendations using Gemini.
        """
    )

st.divider()

st.info(
    "Use the navigation menu in the sidebar to explore "
    "the different modules of the application."
)

st.caption(
    "BIAI AI Internship Round 2 Challenge | "
    "Built with Python, Streamlit, SQLite, and Google Gemini"
)

