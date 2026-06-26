import os
import shutil
import csv
from pathlib import Path

PROJECT_ROOT = Path(r"E:\Working\edu_policy_qa")

EXTERNAL_DIR = PROJECT_ROOT / "data" / "external"
RAW_DOCS_DIR = PROJECT_ROOT / "data" / "raw_docs"
METADATA_DIR = PROJECT_ROOT / "data" / "metadata"
METADATA_FILE = METADATA_DIR / "raw_docs_metadata.csv"

RAW_DOCS_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".txt",
    ".md",
    ".html",
    ".htm",
    ".docx",
    ".csv",
    ".json",
    ".jsonl",
}

SOURCE_MAP = {
    "syllabusqa": "SyllabusQA",
    "umich_syllabus_collection": "UMich Syllabus Collection",
    "macloo_course_syllabi": "macloo Course Syllabi",
}

def infer_doc_type(file_path: Path) -> str:
    name = file_path.name.lower()
    path_text = str(file_path).lower()

    if "syllabus" in name or "syllabus" in path_text:
        return "course syllabus"
    if "assignment" in name or "assignment" in path_text:
        return "assignment description"
    if "rubric" in name or "rubric" in path_text:
        return "grading rubric"
    if "faq" in name or "faq" in path_text:
        return "FAQ"
    if "project" in name or "project" in path_text:
        return "project instructions"
    if "announcement" in name or "announcement" in path_text:
        return "official announcement"
    if file_path.suffix.lower() == ".csv":
        return "dataset csv"
    if file_path.suffix.lower() in [".md", ".html", ".htm"]:
        return "course webpage"
    return "course document"

def infer_source(file_path: Path) -> str:
    path_text = str(file_path).lower()

    for key, value in SOURCE_MAP.items():
        if key.lower() in path_text:
            return value

    return "unknown"

def safe_copy(src: Path, dst_dir: Path) -> Path:
    base_name = src.name
    dst = dst_dir / base_name

    if not dst.exists():
        shutil.copy2(src, dst)
        return dst

    stem = src.stem
    suffix = src.suffix
    counter = 1

    while True:
        new_name = f"{stem}_{counter}{suffix}"
        dst = dst_dir / new_name
        if not dst.exists():
            shutil.copy2(src, dst)
            return dst
        counter += 1

def collect_files():
    collected = []

    for root, dirs, files in os.walk(EXTERNAL_DIR):
        for file in files:
            src_path = Path(root) / file
            ext = src_path.suffix.lower()

            if ext not in ALLOWED_EXTENSIONS:
                continue

            copied_path = safe_copy(src_path, RAW_DOCS_DIR)

            doc_id = copied_path.stem.replace(" ", "_").replace("-", "_").lower()
            source = infer_source(src_path)
            doc_type = infer_doc_type(src_path)

            collected.append({
                "doc_id": doc_id,
                "file_name": copied_path.name,
                "doc_type": doc_type,
                "publication_date": "",
                "source": source,
                "source_url": "",
                "is_official_course_material": "unknown",
                "notes": f"copied from {src_path}"
            })

    return collected

def write_metadata(rows):
    with open(METADATA_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "doc_id",
                "file_name",
                "doc_type",
                "publication_date",
                "source",
                "source_url",
                "is_official_course_material",
                "notes",
            ]
        )
        writer.writeheader()
        writer.writerows(rows)

def main():
    rows = collect_files()
    write_metadata(rows)

    print(f"Collected files: {len(rows)}")
    print(f"Raw docs directory: {RAW_DOCS_DIR}")
    print(f"Metadata file: {METADATA_FILE}")

if __name__ == "__main__":
    main()
