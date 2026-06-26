import pandas as pd
import re
from pathlib import Path

PROJECT_ROOT = Path(r"E:\Working\edu_policy_qa")

INPUT_FILE = PROJECT_ROOT / "data" / "metadata" / "raw_docs_metadata.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "metadata" / "raw_docs_metadata_clean.csv"

SOURCE_URLS = {
    "SyllabusQA": "https://github.com/umass-ml4ed/syllabusqa",
    "UMich Syllabus Collection": "https://github.com/PeterQiu0516/UMich-Syllabus-Collection",
    "macloo Course Syllabi": "https://github.com/macloo/course-syllabi",
}

REMOVE_FILE_PATTERNS = [
    "readme",
    "requirements",
    "playlist",
]

def normalize_text(x):
    if pd.isna(x):
        return ""
    return str(x).strip()

def should_remove(row):
    file_name = normalize_text(row["file_name"]).lower()
    doc_type = normalize_text(row["doc_type"]).lower()

    for pattern in REMOVE_FILE_PATTERNS:
        if pattern in file_name:
            return True

    if file_name.endswith(".csv") or file_name.endswith(".json") or file_name.endswith(".jsonl"):
        return True

    if "dataset" in doc_type:
        return True

    return False

def extract_publication_date(file_name):
    name = file_name.lower()

    season = ""
    year = ""

    if "spring" in name or "_sp" in name or "-sp" in name or " s202" in name:
        season = "Spring"
    elif "fall" in name or "_fa" in name or "-fa" in name or " f202" in name:
        season = "Fall"
    elif "winter" in name or "_wi" in name or "-wi" in name:
        season = "Winter"
    elif "summer" in name or "_su" in name or "-su" in name:
        season = "Summer"

    year_match = re.search(r"(20\d{2})", name)
    if year_match:
        year = year_match.group(1)
    else:
        short_year_match = re.search(r"(?<!\d)(f|s|sp|fa|wi|su)?(\d{2})(?!\d)", name)
        if short_year_match:
            yy = short_year_match.group(2)
            year = "20" + yy

    if season and year:
        return f"{season} {year}"
    if year:
        return year
    return ""

def choose_best_format(df):
    rows = []

    priority = {
        ".txt": 1,
        ".pdf": 2,
        ".docx": 3,
        ".html": 4,
        ".htm": 5,
        ".md": 6,
    }

    df["extension"] = df["file_name"].apply(lambda x: Path(str(x)).suffix.lower())
    df["format_priority"] = df["extension"].map(priority).fillna(99)

    for doc_id, group in df.groupby("doc_id"):
        group = group.sort_values(["format_priority", "file_name"])
        rows.append(group.iloc[0])

    clean_df = pd.DataFrame(rows)
    clean_df = clean_df.drop(columns=["extension", "format_priority"])
    return clean_df

def main():
    df = pd.read_csv(INPUT_FILE)

    for col in [
        "doc_id",
        "file_name",
        "doc_type",
        "publication_date",
        "source",
        "source_url",
        "is_official_course_material",
        "notes",
    ]:
        df[col] = df[col].apply(normalize_text)

    df = df[~df.apply(should_remove, axis=1)].copy()

    df["source_url"] = df["source"].map(SOURCE_URLS).fillna(df["source_url"])

    df["publication_date"] = df.apply(
        lambda row: row["publication_date"] if row["publication_date"] else extract_publication_date(row["file_name"]),
        axis=1
    )

    df["is_official_course_material"] = df["source"].apply(
        lambda x: "yes" if x in SOURCE_URLS else "unknown"
    )

    df["doc_type"] = df["doc_type"].replace("", "course syllabus")

    df = choose_best_format(df)

    df = df.sort_values(["source", "file_name"]).reset_index(drop=True)

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Input rows: {len(pd.read_csv(INPUT_FILE))}")
    print(f"Clean rows: {len(df)}")
    print(f"Saved to: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
