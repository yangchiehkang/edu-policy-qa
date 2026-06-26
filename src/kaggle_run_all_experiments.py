import json
import time
from pathlib import Path

import faiss
import numpy as np
import pandas as pd
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from sentence_transformers import SentenceTransformer


DATA_DIR = Path("/kaggle/input/datasets/williamjkyoung/edu-policy-qa-data")

QUESTIONS_FILE = DATA_DIR / "questions_with_reference.csv"
CHUNKS_FILE = DATA_DIR / "chunks.jsonl"
DOCUMENTS_FILE = DATA_DIR / "documents.jsonl"
FAISS_INDEX_FILE = DATA_DIR / "faiss.index"
METADATA_FILE = DATA_DIR / "chunk_metadata.jsonl"

OUTPUT_DIR = Path("/kaggle/working/results")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

OUTPUT_JSONL = OUTPUT_DIR / "kaggle_all_experiment_results.jsonl"
OUTPUT_CSV = OUTPUT_DIR / "kaggle_all_experiment_results.csv"

MODEL_NAME = "Qwen/Qwen2.5-7B-Instruct"
EMBEDDING_MODEL_NAME = "nomic-ai/nomic-embed-text-v1.5"

TOP_K = 5
MAX_NEW_TOKENS = 256
MAX_CONTEXT_CHARS = 12000
MAX_PASSAGE_CHARS = 1200


def clean_text(text):
    text = str(text)
    text = text.replace("\x00", " ")
    text = text.replace("\xa0", " ")
    text = text.replace("\n", " ")
    text = text.replace("\r", " ")
    text = text.replace("\t", " ")
    text = " ".join(text.split())
    return text.strip()


def load_jsonl(path):
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rows.append(json.loads(line))
    return rows


def get_source(chunk):
    return (
        chunk.get("source_file")
        or chunk.get("source")
        or chunk.get("file_name")
        or chunk.get("filename")
        or chunk.get("doc_id")
        or chunk.get("document_id")
        or ""
    )


def get_page(chunk):
    return (
        chunk.get("page")
        or chunk.get("page_number")
        or chunk.get("page_id")
        or chunk.get("page_idx")
        or ""
    )


def build_full_context(documents):
    parts = []
    for doc in documents:
        source = get_source(doc)
        text = clean_text(doc.get("text", ""))
        parts.append(f"Source: {source}\n{text}")
    full_context = "\n\n".join(parts)
    return full_context[:MAX_CONTEXT_CHARS]


def normalize_embedding(vec):
    arr = np.array(vec, dtype="float32")
    if arr.ndim == 1:
        arr = arr.reshape(1, -1)
    norm = np.linalg.norm(arr, axis=1, keepdims=True)
    norm[norm == 0] = 1.0
    return arr / norm


def retrieve(question, embedder, index, metadata):
    query_embedding = embedder.encode(
        [question],
        convert_to_numpy=True,
        normalize_embeddings=True
    ).astype("float32")

    scores, indices = index.search(query_embedding, TOP_K)

    retrieved = []

    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        chunk = metadata[idx]

        retrieved.append({
            "score": float(score),
            "chunk_id": chunk.get("chunk_id", ""),
            "source": get_source(chunk),
            "page": get_page(chunk),
            "text": clean_text(chunk.get("text", ""))[:MAX_PASSAGE_CHARS]
        })

    return retrieved


def format_retrieved_chunks(retrieved):
    parts = []

    for i, item in enumerate(retrieved, start=1):
        part = (
            f"[Passage {i}]\n"
            f"source: {item['source']}\n"
            f"page: {item['page']}\n"
            f"chunk_id: {item['chunk_id']}\n"
            f"score: {item['score']:.4f}\n"
            f"text: {item['text']}"
        )
        parts.append(part)

    return "\n\n".join(parts)


def generate_answer(tokenizer, model, prompt):
    messages = [
        {
            "role": "user",
            "content": prompt
        }
    ]

    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
        max_length=12000
    ).to(model.device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=MAX_NEW_TOKENS,
            do_sample=False,
            temperature=0.0,
            pad_token_id=tokenizer.eos_token_id
        )

    generated_ids = outputs[0][inputs["input_ids"].shape[-1]:]
    answer = tokenizer.decode(generated_ids, skip_special_tokens=True)

    return answer.strip()


def make_closed_book_prompt(question):
    return f"""Answer the following question.

Question:
{question}

Answer:"""


def make_full_context_prompt(question, full_context):
    return f"""You are answering questions based only on the provided course documents.

Use only the information in the documents.
If the documents do not contain enough evidence, say that the documents do not provide enough information.

Course Documents:
{full_context}

Question:
{question}

Answer:"""


def make_basic_rag_prompt(question, retrieved_chunks_text):
    return f"""You are answering questions based only on the retrieved course document passages.
Use only the information in the passages.
If the passages do not contain enough evidence, say that the documents do not provide enough information.

Retrieved Passages:
{retrieved_chunks_text}

Question:
{question}

Answer:"""


def make_citation_rag_prompt(question, retrieved_chunks_text):
    return f"""You are answering questions based only on the retrieved course document passages.

Rules:
1. Use only the retrieved passages.
2. If the passages do not support an answer, say: "The provided course documents do not specify this."
3. Every answer must include at least one citation.
4. A citation must include source, page, and chunk_id.
5. Do not guess or use outside knowledge.

Retrieved Passages:
{retrieved_chunks_text}

Question:
{question}

Please answer in the following format:

Answer:
Evidence:
- [source: ..., page: ..., chunk_id: ...] ...
Confidence:"""


def write_jsonl_record(record):
    with open(OUTPUT_JSONL, "a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def main():
    if OUTPUT_JSONL.exists():
        OUTPUT_JSONL.unlink()

    print("Loading questions...")
    questions = pd.read_csv(QUESTIONS_FILE, dtype=str).fillna("")

    print("Loading documents...")
    documents = load_jsonl(DOCUMENTS_FILE)
    full_context = build_full_context(documents)

    print("Loading metadata...")
    metadata = load_jsonl(METADATA_FILE)

    print("Loading FAISS index...")
    index = faiss.read_index(str(FAISS_INDEX_FILE))

    print("Loading embedding model...")
    embedder = SentenceTransformer(
        EMBEDDING_MODEL_NAME,
        trust_remote_code=True
    )

    print("Loading generation model...")
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
        bnb_4bit_quant_type="nf4"
    )

    tokenizer = AutoTokenizer.from_pretrained(
        MODEL_NAME,
        trust_remote_code=True
    )

    model = AutoModelForCausalLM.from_pretrained(
        MODEL_NAME,
        quantization_config=quant_config,
        device_map="auto",
        trust_remote_code=True
    )

    all_records = []

    settings = [
        "closed_book",
        "full_context",
        "basic_rag",
        "citation_rag"
    ]

    total = len(questions) * len(settings)
    current = 0

    for _, row in questions.iterrows():
        qid = row["question_id"]
        question = row["question"]

        retrieved = retrieve(question, embedder, index, metadata)
        retrieved_chunks_text = format_retrieved_chunks(retrieved)

        for setting in settings:
            current += 1
            print(f"[{current}/{total}] question_id={qid}, setting={setting}", flush=True)

            if setting == "closed_book":
                prompt = make_closed_book_prompt(question)
                retrieved_for_output = []

            elif setting == "full_context":
                prompt = make_full_context_prompt(question, full_context)
                retrieved_for_output = []

            elif setting == "basic_rag":
                prompt = make_basic_rag_prompt(question, retrieved_chunks_text)
                retrieved_for_output = retrieved

            elif setting == "citation_rag":
                prompt = make_citation_rag_prompt(question, retrieved_chunks_text)
                retrieved_for_output = retrieved

            else:
                prompt = question
                retrieved_for_output = []

            try:
                model_answer = generate_answer(tokenizer, model, prompt)
                error = ""

            except Exception as e:
                model_answer = ""
                error = str(e)

            record = {
                "question_id": qid,
                "category": row.get("category", ""),
                "answerable": row.get("answerable", ""),
                "setting": setting,
                "question": question,
                "model_answer": model_answer,
                "retrieved_chunks": retrieved_for_output,
                "reference_answer": row.get("reference_answer", ""),
                "evidence_doc": row.get("evidence_doc", ""),
                "model_name": MODEL_NAME,
                "error": error
            }

            all_records.append(record)
            write_jsonl_record(record)

            pd.DataFrame(all_records).to_csv(
                OUTPUT_CSV,
                index=False,
                encoding="utf-8-sig"
            )

            time.sleep(0.2)

    pd.DataFrame(all_records).to_csv(
        OUTPUT_CSV,
        index=False,
        encoding="utf-8-sig"
    )

    print("Done.")
    print(f"Saved JSONL to: {OUTPUT_JSONL}")
    print(f"Saved CSV to: {OUTPUT_CSV}")
    print(f"Total records: {len(all_records)}")
    print(f"Error records: {sum(1 for r in all_records if r['error'])}")


if __name__ == "__main__":
    main()
