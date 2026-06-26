import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(r"E:\Working\edu_policy_qa")

QUESTION_FILE = PROJECT_ROOT / "data" / "questions" / "questions_with_reference.csv"

EXPECTED_COUNTS = {
    "factual_extraction": 20,
    "rule_understanding": 20,
    "multi_condition_reasoning": 15,
    "exception_handling": 15,
    "unanswerable_insufficient_evidence": 10,
}

REQUIRED_COLUMNS = [
    "question_id",
    "question",
    "category",
    "reference_answer",
    "evidence_doc",
    "evidence_page",
    "evidence_text",
    "answerable",
    "notes",
]

def main():
    df = pd.read_csv(QUESTION_FILE)

    print("Total rows:", len(df))
    print()

    print("Column check:")
    for col in REQUIRED_COLUMNS:
        print(f"{col}: {'OK' if col in df.columns else 'MISSING'}")

    print()
    print("Category counts:")
    counts = df["category"].value_counts()

    for category, expected in EXPECTED_COUNTS.items():
        actual = int(counts.get(category, 0))
        status = "OK" if actual == expected else "CHECK"
        print(f"{category}: {actual} / expected {expected} [{status}]")

    print()
    print("Missing value check:")

    required_for_all = [
        "question_id",
        "question",
        "category",
        "reference_answer",
        "answerable",
    ]

    for col in required_for_all:
        missing = df[col].isna().sum() + (df[col].astype(str).str.strip() == "").sum()
        print(f"{col}: missing {missing}")

    print()
    print("Answerable value check:")
    print(df["answerable"].value_counts(dropna=False))

    print()
    print("Duplicate question_id:")
    print(df[df["question_id"].duplicated(keep=False)][["question_id", "question"]])

if __name__ == "__main__":
    main()
