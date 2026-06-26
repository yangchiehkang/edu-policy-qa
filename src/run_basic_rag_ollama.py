import json
import time
import urllib.request
import urllib.error
from pathlib import Path

import faiss
import numpy as np
import pandas as pd


PROJECT_ROOT = Path(r"E:\Working\edu_policy_qa")

QUESTIONS_FILE = PROJECT_ROOT / "data" / "questions" / "questions_with_reference.csv"

VECTOR_DIR = PROJECT_ROOT / "data" / "vector_store"
INDEX_FILE = VECTOR_DIR / "faiss.index"
METADATA_FILE = VECTOR_DIR / "chunk_metadata.jsonl"

OUTPUT_DIR = PROJECT_ROOT / "data" / "results"
OUTPUT_FILE = OUTPUT_DIR / "basic_rag_results.csv"

OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embeddings"
OLLAMA_GENERATE_URL = "http://localhost:11434/api/generate"

EMBEDDING_MODEL_NAME = "nomic-embed-text"
LLM_MODEL_NAME = "qwen2.5:3b"

TOP_K = 5
MAX_QUERY_CHARS = 2000


PROMPT_TEMPLATE = """You are answering questions based only on the retrieved course document passages.
Use only the information in the passages.
If the passages do not contain enough evidence, say that the documents do not provide enough information.

Retrieved Passages:
{retrieved_chunks}

Question:
{question}

Answer:"""


def clean_text(text):
    text = str(text)

    replacements = {
        "\x00": " ",
        "\xa0": " ",
        "\xa5": " - ",
        "\u2022": " - ",
        "\uf0b7": " - ",
        "\r": " ",
        "\n": " ",
        "\t": " "
    }

    for old, new in replacements.items():
        text = text.replace(old, new)

    text = " ".join(text.split())

    return text.strip()


def load_metadata():
    rows = []

    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))

    return rows


def call_ollama_embedding(text):
    text = clean_text(text)[:MAX_QUERY_CHARS]

    payload = {
        "model": EMBEDDING_MODEL_NAME,
        "prompt": text
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_EMBEDDING_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=300) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Embedding HTTPError {e.code}: {body}")

    embedding = result.get("embedding")

    if embedding is None:
        raise ValueError(f"No embedding returned from Ollama: {result}")

    arr = np.array([embedding], dtype="float32")
    norm = np.linalg.norm(arr, axis=1, keepdims=True)
    norm[norm == 0] = 1.0
    arr = arr / norm

    return arr.astype("float32")


def retrieve(question, index, metadata, top_k):
    query_embedding = call_ollama_embedding(question)

    scores, indices = index.search(query_embedding, top_k)

    retrieved_items = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        retrieved_items.append({
            "score": float(score),
            "chunk": metadata[idx]
        })

    return retrieved_items


def format_retrieved_chunks(retrieved_items):
    parts = []

    for rank, item in enumerate(retrieved_items, start=1):
        chunk = item["chunk"]
        score = item["score"]

        chunk_id = chunk.get("chunk_id", "")
        source = (
            chunk.get("source_file")
            or chunk.get("source")
            or chunk.get("file_name")
            or chunk.get("filename")
            or chunk.get("doc_id")
            or chunk.get("document_id")
            or ""
        )
        text = chunk.get("text", "")

        part = (
            f"[Passage {rank}]\n"
            f"chunk_id: {chunk_id}\n"
            f"source: {source}\n"
            f"score: {score:.4f}\n"
            f"text:\n{text}"
        )

        parts.append(part)

    return "\n\n".join(parts)


def call_ollama_generate(question, retrieved_chunks_text):
    prompt = PROMPT_TEMPLATE.format(
        retrieved_chunks=retrieved_chunks_text,
        question=question
    )

    payload = {
        "model": LLM_MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_ctx": 4096
        }
    }

    data = json.dumps(payload, ensure_ascii=False).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_GENERATE_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    try:
        with urllib.request.urlopen(req, timeout=600) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"Generation HTTPError {e.code}: {body}")

    return result.get("response", "").strip()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"Loading FAISS index: {INDEX_FILE}", flush=True)
    index = faiss.read_index(str(INDEX_FILE))

    print(f"Loading metadata: {METADATA_FILE}", flush=True)
    metadata = load_metadata()

    print(f"FAISS vectors: {index.ntotal}", flush=True)
    print(f"Metadata rows: {len(metadata)}", flush=True)

    if index.ntotal != len(metadata):
        raise ValueError(f"Index count {index.ntotal} != metadata count {len(metadata)}")

    df = pd.read_csv(QUESTIONS_FILE, dtype=str).fillna("")

    results = []

    for idx, row in df.iterrows():
        qid = row["question_id"]
        question = row["question"]

        print(f"[{idx + 1}/{len(df)}] Basic RAG question_id={qid}", flush=True)

        try:
            retrieved_items = retrieve(
                question=question,
                index=index,
                metadata=metadata,
                top_k=TOP_K
            )

            retrieved_chunks_text = format_retrieved_chunks(retrieved_items)

            answer = call_ollama_generate(
                question=question,
                retrieved_chunks_text=retrieved_chunks_text
            )

            error = ""

        except Exception as e:
            retrieved_items = []
            retrieved_chunks_text = ""
            answer = ""
            error = str(e)

            print(f"  ERROR: {error}", flush=True)

        retrieved_chunk_ids = [
            item["chunk"].get("chunk_id", "") for item in retrieved_items
        ]

        retrieved_scores = [
            item["score"] for item in retrieved_items
        ]

        retrieved_sources = [
            item["chunk"].get("source_file")
            or item["chunk"].get("source")
            or item["chunk"].get("file_name")
            or item["chunk"].get("filename")
            or item["chunk"].get("doc_id")
            or item["chunk"].get("document_id")
            or ""
            for item in retrieved_items
        ]

        results.append({
            "question_id": qid,
            "question": question,
            "category": row.get("category", ""),
            "answerable": row.get("answerable", ""),
            "reference_answer": row.get("reference_answer", ""),
            "evidence_doc": row.get("evidence_doc", ""),
            "rag_answer": answer,
            "top_k": TOP_K,
            "retrieved_chunk_ids": json.dumps(retrieved_chunk_ids, ensure_ascii=False),
            "retrieved_scores": json.dumps(retrieved_scores, ensure_ascii=False),
            "retrieved_sources": json.dumps(retrieved_sources, ensure_ascii=False),
            "retrieved_chunks": retrieved_chunks_text,
            "error": error
        })

        pd.DataFrame(results).to_csv(
            OUTPUT_FILE,
            index=False,
            encoding="utf-8-sig"
        )

        time.sleep(0.2)

    out_df = pd.DataFrame(results)

    out_df.to_csv(
        OUTPUT_FILE,
        index=False,
        encoding="utf-8-sig"
    )

    print()
    print(f"Saved Basic RAG results to: {OUTPUT_FILE}", flush=True)
    print(f"Total rows: {len(out_df)}", flush=True)
    print(f"Error rows: {(out_df['error'].fillna('') != '').sum()}", flush=True)


if __name__ == "__main__":
    main()
