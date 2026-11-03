from services.import_service import import_leads


if __name__ == "__main__":

    result = import_leads()

    print("\nLead Import Summary")
    print("-------------------")

    for key, value in result.items():
        print(f"{key}: {value}")