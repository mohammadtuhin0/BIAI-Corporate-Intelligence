
from services.data_loader import load_leads


def profile_dataset():
    df = load_leads()

    print("\n========== DATASET OVERVIEW ==========")

    print("Total rows:", len(df))
    print("Total columns:", len(df.columns))

    print("\n========== COLUMN NAMES ==========")

    for column in df.columns:
        print(column)

    print("\n========== DATA TYPES ==========")

    print(df.dtypes)

    print("\n========== DATASET INFORMATION ==========")

    df.info()

    print("\n========== MISSING VALUES ==========")

    missing = df.isnull().sum()

    print(missing[missing > 0])

    print(
        "\nTotal missing cells:",
        df.isnull().sum().sum()
    )

    print("\n========== EXACT DUPLICATE ROWS ==========")

    print(df.duplicated().sum())

    print("\n========== UNIQUE COMPANIES ==========")

    print(df["company"].nunique())

    print("\n========== LEADS BY STAGE ==========")

    print(df["stage"].value_counts())

    print("\n========== DEAL VALUE ==========")

    print(
        "Total:",
        df["deal value (BDT)"].sum()
    )

    print(
        "Average:",
        df["deal value (BDT)"].mean()
    )

    print("\n========== DUPLICATE CONTACT EMAILS ==========")

    email = df["contact email"].dropna().str.strip().str.lower()

    duplicate_emails = email[
        email.duplicated(keep=False)
    ].unique()

    print(duplicate_emails)


if __name__ == "__main__":
    profile_dataset()
