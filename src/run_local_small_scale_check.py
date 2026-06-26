import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(r"E:\Working\edu_policy_qa")

QUESTIONS_FILE = PROJECT_ROOT / "data" / "questions" / "questions_with_reference.csv"

RESULTS_DIR = PROJECT_ROOT / "data" / "results"

CLOSED_BOOK_FILE = RESULTS_DIR / "closed_book_llm_results.csv"
FULL_CONTEXT_FILE = RESULTS_DIR / "full_context_prompting_results.csv"
BASIC_RAG_FILE = RESULTS_DIR / "basic_rag_results.csv"
CITATION_RAG_FILE = RESULTS_DIR / "citation_rag_results.csv"

OUTPUT_JSONL = RESULTS_DIR / "local_small_scale_check.jsonl"
OUTPUT_CSV = RESULTS_DIR / "local_small_scale_check.csv"

SAMPLE_SIZE = 20


def read_csv(path):
    return pd.read_csv(path, dtype=str).fillna("")


def has_error(row):
    if "error" not in row:
        return False
    return str(row.get("error", "")).strip() != ""


def check_citation_format(text):
    text = str(text)
    has_answer = "Answer:" in text
    has_evidence = "Evidence:" in text
    has_confidence = "Confidence:" in text
    has_chunk_id = "chunk_id" in text
    return has_answer and has_evidence and has_confidence and has_chunk_id


def main():
    questions = read_csv(QUESTIONS_FILE)
    sample_questions = questions.head(SAMPLE_SIZE)

    closed_df = read_csv(CLOSED_BOOK_FILE)
    full_df = read_csv(FULL_CONTEXT_FILE)
    basic_df = read_csv(BASIC_RAG_FILE)
    citation_df = read_csv(CITATION_RAG_FILE)

    closed_map = closed_df.set_index("question_id").to_dict("index")
    full_map = full_df.set_index("question_id").to_dict("index")
    basic_map = basic_df.set_index("question_id").to_dict("index")
    citation_map = citation_df.set_index("question_id").to_dict("index")

    records = []

    for _, qrow in sample_questions.iterrows():
        qid = qrow["question_id"]

        closed_row = closed_map.get(qid, {})
        full_row = full_map.get(qid, {})
        basic_row = basic_map.get(qid, {})
        citation_row = citation_map.get(qid, {})

        closed_answer = closed_row.get("closed_book_answer", "")
        full_answer = full_row.get("full_context_answer", "")
        basic_answer = basic_row.get("rag_answer", "")
        citation_answer = citation_row.get("citation_rag_answer", "")

        retrieved_chunks = basic_row.get("retrieved_chunks", "")
        retrieved_chunk_ids = basic_row.get("retrieved_chunk_ids", "")

        record = {
            "question_id": qid,
            "category": qrow.get("category", ""),
            "answerable": qrow.get("answerable", ""),

            "closed_book_has_output": bool(str(closed_answer).strip()),
            "full_context_has_output": bool(str(full_answer).strip()),
            "basic_rag_has_output": bool(str(basic_answer).strip()),
            "citation_rag_has_output": bool(str(citation_answer).strip()),

            "closed_book_error": closed_row.get("error", ""),
            "full_context_error": full_row.get("error", ""),
            "basic_rag_error": basic_row.get("error", ""),
            "citation_rag_error": citation_row.get("error", ""),

            "basic_rag_has_retrieved_chunks": bool(str(retrieved_chunks).strip()),
            "basic_rag_has_retrieved_chunk_ids": bool(str(retrieved_chunk_ids).strip()),

            "citation_format_valid": check_citation_format(citation_answer),

            "closed_book_pass": bool(str(closed_answer).strip()) and not has_error(closed_row),
            "full_context_pass": bool(str(full_answer).strip()) and not has_error(full_row),
            "basic_rag_pass": bool(str(basic_answer).strip()) and bool(str(retrieved_chunks).strip()) and not has_error(basic_row),
            "citation_rag_pass": bool(str(citation_answer).strip()) and check_citation_format(citation_answer) and not has_error(citation_row)
        }

        record["all_settings_pass"] = (
            record["closed_book_pass"]
            and record["full_context_pass"]
            and record["basic_rag_pass"]
            and record["citation_rag_pass"]
        )

        records.append(record)

    out_df = pd.DataFrame(records)

    out_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

    with open(OUTPUT_JSONL, "w", encoding="utf-8") as f:
        for record in records:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Saved CSV to: {OUTPUT_CSV}")
    print(f"Saved JSONL to: {OUTPUT_JSONL}")
    print(f"Sample questions: {len(out_df)}")
    print(f"All settings pass: {int(out_df['all_settings_pass'].sum())}/{len(out_df)}")

    print()
    print("Pass count by setting:")
    print("closed_book_pass:", int(out_df["closed_book_pass"].sum()))
    print("full_context_pass:", int(out_df["full_context_pass"].sum()))
    print("basic_rag_pass:", int(out_df["basic_rag_pass"].sum()))
    print("citation_rag_pass:", int(out_df["citation_rag_pass"].sum()))

    print()
    print("Failed rows:")
    failed = out_df[out_df["all_settings_pass"] == False]
    print(failed[[
        "question_id",
        "closed_book_pass",
        "full_context_pass",
        "basic_rag_pass",
        "citation_rag_pass"
    ]])


if __name__ == "__main__":
    main()
