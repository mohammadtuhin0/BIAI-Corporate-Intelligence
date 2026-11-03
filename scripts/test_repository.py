
from database.lead_repository import (
    get_all_leads,
    get_lead_by_id,
)


if __name__ == "__main__":

    leads = get_all_leads()

    print("Total Leads:", len(leads))

    if leads:
        print("\nFirst Lead:")
        print(leads[0])

        lead = get_lead_by_id(leads[0]["lead_id"])

        print("\nSearch by ID:")
        print(lead)
