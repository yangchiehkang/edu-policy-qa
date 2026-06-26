import json
import time
import urllib.request
import urllib.error
from pathlib import Path

import numpy as np


PROJECT_ROOT = Path(r"E:\Working\edu_policy_qa")

CHUNKS_FILE = PROJECT_ROOT / "data" / "processed_docs" / "chunks.jsonl"

VECTOR_DIR = PROJECT_ROOT / "data" / "vector_store"
EMBEDDINGS_FILE = VECTOR_DIR / "chunk_embeddings.npy"
METADATA_FILE = VECTOR_DIR / "chunk_metadata.jsonl"
ERROR_FILE = VECTOR_DIR / "embedding_errors.jsonl"

OLLAMA_EMBEDDING_URL = "http://localhost:11434/api/embeddings"
EMBEDDING_MODEL_NAME = "nomic-embed-text"

MAX_TEXT_CHARS = 2000
RETRY_TIMES = 3
SLEEP_SECONDS = 0.2

TEXT_KEYS = [
    "chunk_text",
    "text",
    "content",
    "page_content",
    "document_text",
    "raw_text"
]


def get_text(row):
    for key in TEXT_KEYS:
        value = row.get(key, "")
        if value:
            return str(value)
    return ""


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


def load_chunks():
    chunks = []

    print(f"Reading chunks from: {CHUNKS_FILE}", flush=True)

    with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
        for line_idx, line in enumerate(f):
            if not line.strip():
                continue

            row = json.loads(line)
            text = get_text(row)
            text = clean_text(text)

            if not text:
                print(f"Warning: no text found at line {line_idx}", flush=True)
                continue

            row["chunk_id"] = row.get("chunk_id", f"chunk_{line_idx:06d}")
            row["text"] = text
            row["embedding_text_len"] = len(text)
            row["embedding_text_truncated"] = len(text) > MAX_TEXT_CHARS

            chunks.append(row)

    return chunks


def call_ollama_embedding(text):
    text = clean_text(text)

    if len(text) > MAX_TEXT_CHARS:
        text = text[:MAX_TEXT_CHARS]

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
        raise RuntimeError(f"HTTPError {e.code}: {body}")

    embedding = result.get("embedding")

    if embedding is None:
        raise ValueError(f"No embedding returned from Ollama. Response: {result}")

    return embedding


def get_embedding_with_retry(text, chunk_id):
    last_error = ""

    for attempt in range(1, RETRY_TIMES + 1):
        try:
            return call_ollama_embedding(text)
        except Exception as e:
            last_error = str(e)
            print(
                f"  Retry {attempt}/{RETRY_TIMES} failed for {chunk_id}: {last_error}",
                flush=True
            )
            time.sleep(1.0)

    raise RuntimeError(last_error)


def normalize_embeddings(embeddings):
    arr = np.array(embeddings, dtype="float32")
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    arr = arr / norms
    return arr.astype("float32")


def save_jsonl(path, rows):
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def main():
    print("Starting Ollama embedding construction...", flush=True)

    VECTOR_DIR.mkdir(parents=True, exist_ok=True)

    if not CHUNKS_FILE.exists():
        raise FileNotFoundError(f"Chunks file not found: {CHUNKS_FILE}")

    chunks = load_chunks()

    print(f"Loaded chunks: {len(chunks)}", flush=True)
    print(f"Max text chars for embedding: {MAX_TEXT_CHARS}", flush=True)

    if len(chunks) == 0:
        raise ValueError("No chunks loaded.")

    embeddings = []
    errors = []
    embedding_dim = None

    for idx, chunk in enumerate(chunks):
        chunk_id = chunk["chunk_id"]
        text = chunk["text"]
        used_text = text[:MAX_TEXT_CHARS]

        print(
            f"[{idx + 1}/{len(chunks)}] Embedding chunk_id={chunk_id}, original_len={len(text)}, used_len={len(used_text)}",
            flush=True
        )

        try:
            emb = get_embedding_with_retry(used_text, chunk_id)

            if embedding_dim is None:
                embedding_dim = len(emb)
                print(f"Detected embedding dimension: {embedding_dim}", flush=True)

            embeddings.append(emb)

        except Exception as e:
            error_msg = str(e)

            print(f"  ERROR: failed chunk_id={chunk_id}: {error_msg}", flush=True)

            errors.append({
                "index": idx,
                "chunk_id": chunk_id,
                "text_len": len(text),
                "used_len": len(used_text),
                "error": error_msg
            })

            if embedding_dim is None:
                print("  Getting fallback embedding dimension from test prompt...", flush=True)
                test_emb = call_ollama_embedding("test")
                embedding_dim = len(test_emb)
                print(f"Detected embedding dimension: {embedding_dim}", flush=True)

            embeddings.append([0.0] * embedding_dim)

        time.sleep(SLEEP_SECONDS)

    embeddings = normalize_embeddings(embeddings)

    print(f"Embedding shape: {embeddings.shape}", flush=True)

    np.save(EMBEDDINGS_FILE, embeddings)
    save_jsonl(METADATA_FILE, chunks)
    save_jsonl(ERROR_FILE, errors)

    print(f"Saved embeddings to: {EMBEDDINGS_FILE}", flush=True)
    print(f"Saved metadata to: {METADATA_FILE}", flush=True)
    print(f"Saved errors to: {ERROR_FILE}", flush=True)
    print(f"Error chunks: {len(errors)}", flush=True)
    print("Done.", flush=True)


if __name__ == "__main__":
    main()
