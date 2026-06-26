import json
import re
from pathlib import Path
from tqdm import tqdm


PROJECT_ROOT = Path(r"E:\Working\edu_policy_qa")

INPUT_FILE = PROJECT_ROOT / "data" / "processed_docs" / "documents.jsonl"
OUTPUT_FILE = PROJECT_ROOT / "data" / "processed_docs" / "chunks.jsonl"

CHUNK_SIZE = 400
CHUNK_OVERLAP = 80


def clean_text(text: str) -> str:
    if text is None:
        return ""

    text = text.replace("\x00", " ")
    text = text.replace("\ufeff", " ")
    text = text.replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def split_words(text: str):
    return text.split()


def infer_section(text: str) -> str:
    lines = [line.strip() for line in text.split("\n") if line.strip()]

    for line in lines[:8]:
        if len(line) <= 80:
            lower = line.lower()

            keywords = [
                "course overview",
                "course description",
                "grading",
                "grades",
                "assignments",
                "attendance",
                "late policy",
                "academic integrity",
                "course policies",
                "schedule",
                "requirements",
                "exams",
                "homework",
                "project",
                "office hours",
            ]

            for kw in keywords:
                if kw in lower:
                    return line

            if line.isupper() and len(line.split()) <= 10:
                return line

    return ""


def make_chunks(record):
    text = clean_text(record.get("text", ""))
    words = split_words(text)

    if not words:
        return []

    chunks = []
    start = 0
    chunk_index = 1

    while start < len(words):
        end = min(start + CHUNK_SIZE, len(words))
        chunk_words = words[start:end]
        chunk_text = " ".join(chunk_words).strip()

        if chunk_text:
            chunk_id = f"{record['doc_id']}_p{record['page']}_c{chunk_index}"

            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "doc_id": record.get("doc_id", ""),
                    "source": record.get("source", ""),
                    "doc_type": record.get("doc_type", ""),
                    "publication_date": record.get("publication_date", ""),
                    "data_source": record.get("data_source", ""),
                    "source_url": record.get("source_url", ""),
                    "is_official_course_material": record.get("is_official_course_material", ""),
                    "page": record.get("page", ""),
                    "chunk_index": chunk_index,
                    "start_word": start,
                    "end_word": end,
                    "section": infer_section(chunk_text),
                    "text": chunk_text,
                }
            )

        if end == len(words):
            break

        start = end - CHUNK_OVERLAP
        chunk_index += 1

    return chunks


def main():
    all_chunks = []

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        records = [json.loads(line) for line in f if line.strip()]

    for record in tqdm(records, desc="Chunking documents"):
        chunks = make_chunks(record)
        all_chunks.extend(chunks)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")

    print(f"Input records: {len(records)}")
    print(f"Output chunks: {len(all_chunks)}")
    print(f"Saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
