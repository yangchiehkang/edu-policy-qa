import json
import time
import urllib.request
import urllib.error
import pandas as pd
from pathlib import Path

PROJECT_ROOT = Path(r"E:\Working\edu_policy_qa")

QUESTIONS_FILE = PROJECT_ROOT / "data" / "questions" / "questions_with_reference.csv"
OUTPUT_DIR = PROJECT_ROOT / "data" / "results"
OUTPUT_FILE = OUTPUT_DIR / "closed_book_llm_results.csv"

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "qwen2.5:3b"

PROMPT_TEMPLATE = """You are answering questions about a course policy.
Answer the question as accurately as possible.

Question:
{question}

Answer:"""


def call_ollama(question: str) -> str:
    prompt = PROMPT_TEMPLATE.format(question=question)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.2,
            "num_ctx": 4096
        }
    }

    data = json.dumps(payload).encode("utf-8")

    req = urllib.request.Request(
        OLLAMA_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=300) as response:
        result = json.loads(response.read().decode("utf-8"))

    return result.get("response", "").strip()


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    df = pd.read_csv(QUESTIONS_FILE, dtype=str).fillna("")

    results = []

    for idx, row in df.iterrows():
        qid = row["question_id"]
        question = row["question"]

        print(f"[{idx + 1}/{len(df)}] Running local closed-book LLM for {qid}")

        try:
            answer = call_ollama(question)
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
            "closed_book_answer": answer,
            "error": error,
        })

        temp_df = pd.DataFrame(results)
        temp_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

        time.sleep(0.2)

    out_df = pd.DataFrame(results)
    out_df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print()
    print(f"Saved closed-book results to: {OUTPUT_FILE}")
    print(f"Total rows: {len(out_df)}")
    print(f"Error rows: {(out_df['error'].fillna('') != '').sum()}")


if __name__ == "__main__":
    main()
