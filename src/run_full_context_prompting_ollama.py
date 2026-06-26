import json
import time
import urllib.request
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(r"E:\Working\edu_policy_qa")

QUESTIONS_FILE = PROJECT_ROOT / "data" / "questions" / "questions_with_reference.csv"
DOCS_FILE = PROJECT_ROOT / "data" / "processed_docs" / "documents.jsonl"

OUTPUT_DIR = PROJECT_ROOT / "data" / "results"
OUTPUT_FILE = OUTPUT_DIR / "full_context_prompting_results.csv"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"

MAX_CONTEXT_CHARS = 12000

PROMPT_TEMPLATE = """You are answering questions based only on the provided course documents.
If the answer is not stated in the documents, say that the documents do not provide enough information.

Course Documents:
{full_context}

Question:
{question}

Answer:"""


TEXT_KEYS = [
    "text",
    "content",
    "page_content",
    "document_text",
    "raw_text"
]

DOC_ID_KEYS = [
    "doc_id",
    "document_id",
    "source",
    "source_file",
    "file_name",
    "filename",
    "path",
    "title",
    "name"
]


def normalize(value: str) -> str:
    return str(value).lower().replace("\\", "/").strip()


def get_first_existing(row: dict, keys: list[str]) -> str:
    for key in keys:
        value = row.get(key, "")
        if value:
            return str(value)
    return ""


def load_documents():
    docs = []

    with open(DOCS_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue

            row = json.loads(line)

            text = get_first_existing(row, TEXT_KEYS)
            doc_label = get_first_existing(row, DOC_ID_KEYS)

            if not text:
                continue

            doc_key_parts = []
            for key in DOC_ID_KEYS:
                if row.get(key):
                    doc_key_parts.append(str(row.get(key)))

            doc_key = " | ".join(doc_key_parts)

            docs.append({
                "doc_label": doc_label,
                "doc_key": doc_key,
                "text": text
            })

    return docs


def truncate_context(context: str) -> str:
    if len(context) <= MAX_CONTEXT_CHARS:
        return context

    return context[:MAX_CONTEXT_CHARS]


def select_context(question_row, docs):
    evidence_doc = str(question_row.get("evidence_doc", "")).strip()
    evidence_doc_norm = normalize(evidence_doc)

    invalid_values = {
        "",
        "nan",
        "none",
        "n/a",
        "na",
        "insufficient_evidence",
        "not_applicable"
    }

    selected_docs = []

    if evidence_doc_norm not in invalid_values:
        for doc in docs:
            doc_key_norm = normalize(doc["doc_key"])
            doc_label_norm = normalize(doc["doc_label"])

            if (
                evidence_doc_norm in doc_key_norm
                or evidence_doc_norm in doc_label_norm
                or doc_label_norm in evidence_doc_norm
            ):
                selected_docs.append(doc)

    if not selected_docs:
        selected_docs = docs

    context_parts = []

    for idx, doc in enumerate(selected_docs, start=1):
        part = f"[Document {idx}: {doc['doc_label']}]\n{doc['text']}"
        context_parts.append(part)

        current_context = "\n\n".join(context_parts)
        if len(current_context) >= MAX_CONTEXT_CHARS:
            break

    full_context = "\n\n".join(context_parts)
    return truncate_context(full_context), len(selected_docs)


def call_ollama(question: str, full_context: str) -> str:
    prompt = PROMPT_TEMPLATE.format(
        full_context=full_context,
        question=question
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_ctx": 16384
        }
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=600) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result.get("response", "").strip()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    docs = load_documents()
    print(f"Loaded documents: {len(docs)}")

    df = pd.read_csv(QUESTIONS_FILE, dtype=str).fillna("")

    results = []

    for idx, row in df.iterrows():
        qid = row["question_id"]
        question = row["question"]

        print(f"[{idx + 1}/{len(df)}] Running full-context prompting for {qid}")

        full_context, selected_doc_count = select_context(row, docs)

        try:
            answer = call_ollama(question, full_context)
            error = ""
        except Exception as e:
            answer = ""
            error = str(e)

        results.append({
            "question_id": qid,
            "question": question,
            "category": row["category"],
            "answerable": row["answerable"],
            "reference_answer": row["reference_answer"],
            "evidence_doc": row.get("evidence_doc", ""),
            "full_context_answer": answer,
            "selected_doc_count": selected_doc_count,
            "context_chars": len(full_context),
            "error": error,
        })

        temp_df = pd.DataFrame(results)
        temp_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

        time.sleep(0.2)

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print()
    print(f"Saved full-context results to: {OUTPUT_FILE}")
    print(f"Total rows: {len(out_df)}")
    print(f"Error rows: {(out_df['error'].fillna('') != '').sum()}")


if __name__ == "__main__":
    main()
