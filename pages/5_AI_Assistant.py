
import streamlit as st

from services.lead_service import list_leads
from services.ai_service import (
    ask_business_question,
    generate_business_summary,
    generate_followup_recommendations,
    generate_lead_insights,
    AIServiceError,
)
from config.settings import is_gemini_configured


st.set_page_config(
    page_title="AI Assistant | BIAI CRM",
    page_icon="🤖",
    layout="wide",
)

st.title("🤖 BIAI AI Business Assistant")
st.caption("Analyze your corporate leads and sales pipeline using Google Gemini.")

if not is_gemini_configured():
    st.error("Gemini API is not configured. Please check your .env file.")
    st.stop()


@st.cache_data(ttl=30)
def load_leads():
    return list_leads()


try:
    leads = load_leads()
except Exception as error:
    st.error(f"Could not load CRM data: {error}")
    st.stop()


if not leads:
    st.warning("No leads found in the database.")
    st.stop()


# Sidebar
with st.sidebar:
    st.subheader("📊 CRM Overview")
    st.metric("Total Leads", len(leads))

    total_value = sum(float(lead.get("deal_value") or 0) for lead in leads)
    st.metric("Total Deal Value", f"৳{total_value:,.0f}")

    st.divider()
    st.caption("AI powered by Google Gemini")


# Quick AI actions
st.subheader("⚡ Quick AI Analysis")

col1, col2, col3 = st.columns(3)

def run_ai_action(action, label):
    with st.spinner(f"Generating {label}..."):
        try:
            result = action(leads)
            st.session_state.ai_result = result
            st.session_state.ai_result_title = label
            st.session_state.ai_error = None
        except AIServiceError as error:
            st.session_state.ai_error = str(error)


with col1:
    if st.button("📈 Business Summary", use_container_width=True):
        run_ai_action(generate_business_summary, "Business Summary")

with col2:
    if st.button("📅 Follow-up Recommendations", use_container_width=True):
        run_ai_action(
            generate_followup_recommendations,
            "Follow-up Recommendations",
        )

with col3:
    if st.button("💡 Lead Insights", use_container_width=True):
        run_ai_action(generate_lead_insights, "Lead Insights")


if st.session_state.get("ai_error"):
    st.error(st.session_state.ai_error)

if st.session_state.get("ai_result"):
    st.subheader(st.session_state.ai_result_title)
    st.markdown(st.session_state.ai_result)


st.divider()


# Ask AI
st.subheader("💬 Ask Your Business Question")
st.write(
    "Ask questions about leads, sales performance, industries, "
    "deal values, and follow-up priorities."
)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


with st.form("ai_question_form", clear_on_submit=True):
    question = st.text_area(
        "Your question",
        placeholder="Example: Which leads should we prioritize this week?",
        height=100,
    )
    submitted = st.form_submit_button(
        "Ask AI 🚀",
        use_container_width=True,
    )


if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        st.session_state.chat_history.append(
            {"role": "user", "content": question.strip()}
        )

        with st.spinner("Gemini is analyzing your CRM data..."):
            try:
                answer = ask_business_question(question.strip(), leads)

                st.session_state.chat_history.append(
                    {"role": "assistant", "content": answer}
                )
            except AIServiceError as error:
                st.session_state.chat_history.append(
                    {
                        "role": "assistant",
                        "content": f"Sorry, I couldn't generate an answer: {error}",
                    }
                )

        st.rerun()


if st.session_state.chat_history:
    if st.button("🗑️ Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()


st.divider()

st.caption(
    "Privacy note: The AI service sends selected business fields "
    "(company, industry, stage, deal value, source and dates) "
    "to Google Gemini. Contact names, emails, phone numbers and notes "
    "are not included in the AI context."
)
