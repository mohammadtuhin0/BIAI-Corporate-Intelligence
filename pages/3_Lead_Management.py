
import streamlit as st
import pandas as pd

from services.lead_service import (
    list_leads,
    find_lead,
    create_new_lead,
    update_existing_lead,
    remove_lead,
)


st.set_page_config(
    page_title="Lead Management | BIAI CRM",
    page_icon="👥",
    layout="wide",
)


st.title("👥 Lead Management")
st.caption("Manage corporate leads from one place.")

st.divider()


# --------------------------------------------------
# Load Leads
# --------------------------------------------------

try:
    leads = list_leads()
    df = pd.DataFrame(leads)

except Exception as error:
    st.error(f"Unable to load leads: {error}")
    st.stop()


# --------------------------------------------------
# Search and Filter
# --------------------------------------------------

st.subheader("Search & Filter Leads")

col1, col2 = st.columns(2)

with col1:
    search_query = st.text_input(
        "Search by company or Lead ID",
        placeholder="Enter company name or Lead ID...",
    )

with col2:
    stages = [
        "All",
        "New",
        "Contacted",
        "Meeting",
        "Proposal",
        "Invoice sent",
        "Paid",
        "Lost",
    ]

    selected_stage = st.selectbox(
        "Filter by Stage",
        stages,
    )


filtered_df = df.copy()

if search_query:
    search_mask = (
        filtered_df["company"].str.contains(
            search_query,
            case=False,
            na=False,
        )
        |
        filtered_df["lead_id"].str.contains(
            search_query,
            case=False,
            na=False,
        )
    )

    filtered_df = filtered_df[search_mask]


if selected_stage != "All":
    filtered_df = filtered_df[
        filtered_df["stage"] == selected_stage
    ]


st.write(f"Showing **{len(filtered_df)}** of **{len(df)}** leads.")


# --------------------------------------------------
# Lead Table
# --------------------------------------------------

st.subheader("Corporate Leads")

if not filtered_df.empty:

    display_columns = [
        "lead_id",
        "company",
        "industry",
        "contact_name",
        "contact_email",
        "stage",
        "deal_value",
        "next_followup",
    ]

    st.dataframe(
        filtered_df[display_columns],
        use_container_width=True,
        hide_index=True,
    )

else:
    st.info("No leads found matching your search.")


st.divider()


# --------------------------------------------------
# Create New Lead
# --------------------------------------------------

st.subheader("➕ Add New Lead")

with st.expander("Create a new corporate lead"):

    with st.form("create_lead_form"):

        col1, col2 = st.columns(2)

        with col1:
            new_lead_id = st.text_input("Lead ID")
            new_company = st.text_input("Company Name")
            new_industry = st.text_input("Industry")
            new_contact_name = st.text_input("Contact Name")
            new_contact_role = st.text_input("Contact Role")
            new_contact_email = st.text_input("Contact Email")
            new_contact_phone = st.text_input("Contact Phone")

        with col2:
            new_source = st.text_input("Lead Source")

            new_stage = st.selectbox(
                "Stage",
                stages[1:],
                index=0,
            )

            new_deal_value = st.number_input(
                "Deal Value (BDT)",
                min_value=0.0,
                value=0.0,
                step=1000.0,
            )

            new_last_contact = st.date_input(
                "Last Contact",
                value=None,
            )

            new_next_followup = st.date_input(
                "Next Follow-up",
                value=None,
            )

        new_notes = st.text_area("Notes")

        submitted = st.form_submit_button(
            "Create Lead",
            use_container_width=True,
        )

        if submitted:

            lead_data = {
                "lead_id": new_lead_id.strip(),
                "company": new_company.strip(),
                "industry": new_industry.strip(),
                "contact_name": new_contact_name.strip(),
                "contact_role": new_contact_role.strip(),
                "contact_email": new_contact_email.strip(),
                "contact_phone": new_contact_phone.strip(),
                "source": new_source.strip(),
                "stage": new_stage,
                "deal_value": new_deal_value,
                "last_contact": (
                    str(new_last_contact)
                    if new_last_contact else None
                ),
                "next_followup": (
                    str(new_next_followup)
                    if new_next_followup else None
                ),
                "notes": new_notes.strip(),
            }

            try:
                create_new_lead(lead_data)

                st.success(
                    f"Lead {new_lead_id} created successfully!"
                )

                st.rerun()

            except Exception as error:
                st.error(f"Unable to create lead: {error}")


st.divider()


# --------------------------------------------------
# Update Existing Lead
# --------------------------------------------------

st.subheader("✏️ Update Existing Lead")

lead_ids = df["lead_id"].tolist()

if lead_ids:

    selected_lead_id = st.selectbox(
        "Select Lead ID to Update",
        lead_ids,
        key="update_lead_selector",
    )

    selected_lead = find_lead(selected_lead_id)

    if selected_lead:

        with st.form("update_lead_form"):

            col1, col2 = st.columns(2)

            with col1:
                edit_company = st.text_input(
                    "Company Name",
                    value=selected_lead["company"] or "",
                )

                edit_industry = st.text_input(
                    "Industry",
                    value=selected_lead["industry"] or "",
                )

                edit_contact_name = st.text_input(
                    "Contact Name",
                    value=selected_lead["contact_name"] or "",
                )

                edit_contact_role = st.text_input(
                    "Contact Role",
                    value=selected_lead["contact_role"] or "",
                )

                edit_email = st.text_input(
                    "Contact Email",
                    value=selected_lead["contact_email"] or "",
                )

                edit_phone = st.text_input(
                    "Contact Phone",
                    value=selected_lead["contact_phone"] or "",
                )

            with col2:
                edit_source = st.text_input(
                    "Lead Source",
                    value=selected_lead["source"] or "",
                )

                edit_stage = st.selectbox(
                    "Stage",
                    stages[1:],
                    index=stages[1:].index(
                        selected_lead["stage"]
                    ),
                )

                edit_deal_value = st.number_input(
                    "Deal Value (BDT)",
                    min_value=0.0,
                    value=float(selected_lead["deal_value"] or 0),
                    step=1000.0,
                )

                edit_last_contact = st.text_input(
                    "Last Contact (YYYY-MM-DD)",
                    value=selected_lead["last_contact"] or "",
                )

                edit_next_followup = st.text_input(
                    "Next Follow-up (YYYY-MM-DD)",
                    value=selected_lead["next_followup"] or "",
                )

            edit_notes = st.text_area(
                "Notes",
                value=selected_lead["notes"] or "",
            )

            update_submitted = st.form_submit_button(
                "Update Lead",
                use_container_width=True,
            )

            if update_submitted:

                updated_data = {
                    "company": edit_company.strip(),
                    "industry": edit_industry.strip(),
                    "contact_name": edit_contact_name.strip(),
                    "contact_role": edit_contact_role.strip(),
                    "contact_email": edit_email.strip(),
                    "contact_phone": edit_phone.strip(),
                    "source": edit_source.strip(),
                    "stage": edit_stage,
                    "deal_value": edit_deal_value,
                    "last_contact": edit_last_contact.strip() or None,
                    "next_followup": edit_next_followup.strip() or None,
                    "notes": edit_notes.strip(),
                }

                try:
                    update_existing_lead(
                        selected_lead_id,
                        updated_data,
                    )

                    st.success(
                        f"Lead {selected_lead_id} updated successfully!"
                    )

                    st.rerun()

                except Exception as error:
                    st.error(f"Unable to update lead: {error}")


st.divider()


# --------------------------------------------------
# Delete Lead
# --------------------------------------------------

st.subheader("🗑️ Delete Lead")

with st.expander("Delete a corporate lead"):

    delete_lead_id = st.selectbox(
        "Select Lead ID to Delete",
        lead_ids,
        key="delete_lead_selector",
    )

    confirm_delete = st.checkbox(
        "I confirm that I want to permanently delete this lead."
    )

    if st.button(
        "Delete Selected Lead",
        type="secondary",
        disabled=not confirm_delete,
    ):

        try:
            remove_lead(delete_lead_id)

            st.success(
                f"Lead {delete_lead_id} deleted successfully!"
            )

            st.rerun()

        except Exception as error:
            st.error(f"Unable to delete lead: {error}")
