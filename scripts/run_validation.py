
from services.data_loader import load_leads

from services.validation_service import (
    validate_leads,
    generate_quality_summary,
)


def main():

    df = load_leads()

    issues = validate_leads(df)

    summary = generate_quality_summary(issues)

    print("\n========== DATA QUALITY REPORT ==========")

    for key, value in summary.items():
        print(f"{key}: {value}")

    print("\n========== ISSUE DISTRIBUTION ==========")

    if not issues.empty:
        print(issues["issue_type"].value_counts())

        print("\n========== DETAILED ISSUES ==========")

        print(
            issues.to_string(index=False)
        )

    else:
        print("No data quality issues found.")

    # Save the report
    output_path = "data/processed/data_quality_report.csv"

    issues.to_csv(output_path, index=False)

    print(f"\nReport saved to: {output_path}")


if __name__ == "__main__":
    main()
