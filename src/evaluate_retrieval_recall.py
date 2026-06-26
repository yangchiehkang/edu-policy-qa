import json
from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(r"E:\Working\edu_policy_qa")

RESULT_FILE = PROJECT_ROOT / "data" / "results" / "basic_rag_results.csv"
OUTPUT_FILE = PROJECT_ROOT / "data" / "results" / "retrieval_recall_results.csv"


def normalize_text(text):
    text = str(text).lower().strip()
    text = text.replace("\\", "/")
    text = " ".join(text.split())
    return text


def parse_json_list(value):
    if pd.isna(value):
        return []

    value = str(value).strip()

    if value == "":
        return []

    try:
        return json.loads(value)
    except Exception:
        return []


def check_evidence_hit(row):
    evidence_doc = normalize_text(row.get("evidence_doc", ""))
    retrieved_sources = parse_json_list(row.get("retrieved_sources", ""))
    retrieved_chunks = normalize_text(row.get("retrieved_chunks", ""))

    retrieved_sources_norm = [
        normalize_text(source) for source in retrieved_sources
    ]

    if evidence_doc == "":
        return False, "no_evidence_doc"

    for source in retrieved_sources_norm:
        if evidence_doc in source or source in evidence_doc:
            return True, "source_match"

    if evidence_doc in retrieved_chunks:
        return True, "chunk_text_match"

    return False, "not_found"


def main():
    df = pd.read_csv(RESULT_FILE, dtype=str).fillna("")

    records = []

    for _, row in df.iterrows():
        question_id = row.get("question_id", "")
        category = row.get("category", "")
        answerable = row.get("answerable", "")
        evidence_doc = row.get("evidence_doc", "")
        retrieved_chunk_ids = row.get("retrieved_chunk_ids", "")
        retrieved_sources = row.get("retrieved_sources", "")

        hit, match_type = check_evidence_hit(row)

        records.append({
            "question_id": question_id,
            "category": category,
            "answerable": answerable,
            "evidence_doc": evidence_doc,
            "retrieved_chunk_ids": retrieved_chunk_ids,
            "retrieved_sources": retrieved_sources,
            "retrieval_hit": hit,
            "match_type": match_type
        })

    out_df = pd.DataFrame(records)

    out_df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    total = len(out_df)
    answerable_df = out_df[out_df["answerable"].astype(str).str.lower().isin(["true", "yes", "1"])]

    total_answerable = len(answerable_df)
    hit_answerable = int(answerable_df["retrieval_hit"].sum())

    if total_answerable > 0:
        recall = hit_answerable / total_answerable
    else:
        recall = 0

    print(f"Saved retrieval recall results to: {OUTPUT_FILE}")
    print(f"Total questions: {total}")
    print(f"Answerable questions: {total_answerable}")
    print(f"Retrieval hits among answerable questions: {hit_answerable}")
    print(f"Retrieval recall@top_k: {recall:.4f}")

    print()
    print("Recall by category:")
    category_stats = answerable_df.groupby("category")["retrieval_hit"].agg(["count", "sum"])
    category_stats["recall"] = category_stats["sum"] / category_stats["count"]
    print(category_stats)


if __name__ == "__main__":
    main()
