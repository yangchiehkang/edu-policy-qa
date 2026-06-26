import numpy as np
import faiss
from pathlib import Path


PROJECT_ROOT = Path(r"E:\Working\edu_policy_qa")

VECTOR_DIR = PROJECT_ROOT / "data" / "vector_store"
EMBEDDINGS_FILE = VECTOR_DIR / "chunk_embeddings.npy"
INDEX_FILE = VECTOR_DIR / "faiss.index"


def main():
    print(f"Loading embeddings from: {EMBEDDINGS_FILE}")

    if not EMBEDDINGS_FILE.exists():
        raise FileNotFoundError(f"Embeddings file not found: {EMBEDDINGS_FILE}")

    embeddings = np.load(EMBEDDINGS_FILE).astype("float32")

    print(f"Embedding shape: {embeddings.shape}")

    dim = embeddings.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(embeddings)

    faiss.write_index(index, str(INDEX_FILE))

    print(f"Saved FAISS index to: {INDEX_FILE}")
    print(f"Total vectors in index: {index.ntotal}")


if __name__ == "__main__":
    main()
