# Edu Policy QA

A Retrieval-Augmented Generation system for education policy and course syllabus question answering.

## Overview

Edu Policy QA is a document question-answering project built around education-related documents such as course syllabi, academic policy files, and teaching documents.

The project compares multiple LLM-based question-answering settings, including:

- Closed-book LLM answering
- Full-context prompting
- Basic RAG
- Citation-based RAG

The goal is to evaluate whether retrieval-augmented generation can produce more accurate and better-grounded answers than directly prompting an LLM without external evidence.

---

## Key Features

- Document collection and metadata cleaning
- PDF / DOCX / TXT document loading
- Text chunking for long education documents
- Embedding generation with local models
- FAISS vector index construction
- Retrieval recall evaluation
- Closed-book LLM baseline
- Full-context prompting baseline
- Basic RAG pipeline
- Citation-based RAG pipeline
- Local experiment scripts
- Kaggle-compatible experiment runner
- Result analysis notebooks

---

## Project Structure

```text
edu-policy-qa/
├─ data/
│  ├─ metadata/              # Dataset source and document metadata
│  ├─ processed_docs/        # Parsed documents and text chunks
│  ├─ questions/             # QA questions with reference answers
│  ├─ outputs/               # Model-generated outputs
│  ├─ results/               # Experiment result files
│  └─ vector_store/          # FAISS index and embedding metadata
│
├─ src/
│  ├─ collect_raw_docs.py
│  ├─ clean_raw_docs_metadata.py
│  ├─ document_loader.py
│  ├─ chunk_documents.py
│  ├─ build_embeddings_ollama.py
│  ├─ build_faiss_index.py
│  ├─ evaluate_retrieval_recall.py
│  ├─ run_closed_book_llm_ollama.py
│  ├─ run_full_context_prompting_ollama.py
│  ├─ run_basic_rag_ollama.py
│  ├─ run_citation_rag_ollama.py
│  ├─ kaggle_run_all_experiments.py
│  └─ validate_questions.py
│
├─ notebooks/
│  ├─ 01_data_preparation.ipynb
│  ├─ 02_build_rag_index.ipynb
│  ├─ 03_run_experiments_local.ipynb
│  ├─ 04_analyze_results.ipynb
│  └─ kaggle_experiment.ipynb
│
├─ reports/
│  └─ progress_log.md
│
├─ results/
│  └─ figures/
│
├─ main.tex
├─ main.pdf
├─ environment.yml
├─ requirements.txt
└─ README.md
```

---

## Methods

### 1. Closed-book LLM

The model answers questions directly without seeing any retrieved documents.

This setting tests how much the model can answer from its internal knowledge only.

### 2. Full-context Prompting

The model receives the relevant full document context in the prompt.

This setting provides an upper-bound style comparison when the document context is directly available.

### 3. Basic RAG

The system retrieves relevant chunks from the document collection and sends them to the LLM as context.

Pipeline:

```text
Question → Embedding → FAISS Retrieval → Top-k Chunks → LLM Answer
```

### 4. Citation RAG

Citation RAG extends basic RAG by requiring the model to answer with supporting citations from retrieved document chunks.

Pipeline:

```text
Question → Retrieval → Evidence Chunks → LLM Answer + Citation
```

This setting is designed to improve answer grounding and make the output easier to verify.

---

## Dataset

The project uses education-related documents, including:

- Course syllabi
- Academic course descriptions
- Teaching policy documents
- University course materials

The raw document collection includes files in:

- PDF
- DOCX
- TXT

For GitHub release, large raw documents, external datasets, and generated vector indexes are not included. They should be prepared or regenerated locally.

---

## Experiments

The project evaluates several QA strategies:

| Method | Description |
|---|---|
| Closed-book LLM | Answers without retrieved evidence |
| Full-context Prompting | Uses full document context |
| Basic RAG | Retrieves relevant chunks before answering |
| Citation RAG | Retrieves chunks and generates citation-supported answers |

The main evaluation focuses on:

- Retrieval recall
- Answer correctness
- Citation quality
- Evidence grounding
- Robustness across different question types

---

## Results

Experiment outputs are stored under:

```text
data/results/
data/outputs/
```

Main result files include:

```text
closed_book_llm_results.csv
full_context_prompting_results.csv
basic_rag_results.csv
citation_rag_results.csv
retrieval_recall_results.csv
kaggle_all_experiment_results.csv
```

These files compare different QA methods and help analyze whether RAG improves education-document question answering.

---

## How to Run

### 1. Install dependencies

Using pip:

```bash
pip install -r requirements.txt
```

Or using conda:

```bash
conda env create -f environment.yml
conda activate edu-policy-qa
```

---

### 2. Prepare documents

Place raw education documents under:

```text
data/raw_docs/
```

Then collect and clean metadata:

```bash
python src/collect_raw_docs.py
python src/clean_raw_docs_metadata.py
```

---

### 3. Parse and chunk documents

```bash
python src/chunk_documents.py
```

This creates document chunks for retrieval.

---

### 4. Build embeddings

```bash
python src/build_embeddings_ollama.py
```

---

### 5. Build FAISS index

```bash
python src/build_faiss_index.py
```

---

### 6. Evaluate retrieval

```bash
python src/evaluate_retrieval_recall.py
```

---

### 7. Run QA experiments

Closed-book baseline:

```bash
python src/run_closed_book_llm_ollama.py
```

Full-context prompting:

```bash
python src/run_full_context_prompting_ollama.py
```

Basic RAG:

```bash
python src/run_basic_rag_ollama.py
```

Citation RAG:

```bash
python src/run_citation_rag_ollama.py
```

Run all experiments:

```bash
python src/kaggle_run_all_experiments.py
```

---

## Notebooks

The notebooks provide a step-by-step workflow:

| Notebook | Purpose |
|---|---|
| `01_data_preparation.ipynb` | Prepare and inspect documents |
| `02_build_rag_index.ipynb` | Build embeddings and FAISS index |
| `03_run_experiments_local.ipynb` | Run QA experiments locally |
| `04_analyze_results.ipynb` | Analyze experiment results |
| `kaggle_experiment.ipynb` | Kaggle-compatible experiment workflow |

---

## Important Notes

This repository is intended for research and educational purposes.

The public GitHub version does not include:

- Full external datasets
- Large raw PDF / DOCX files
- Generated FAISS indexes
- Large embedding files
- Private local experiment caches

These files can be regenerated using the provided scripts.

---

## Technologies Used

- Python
- FAISS
- Ollama
- Local LLM inference
- Embedding-based retrieval
- Retrieval-Augmented Generation
- Citation-based QA
- Pandas
- Jupyter Notebook
- LaTeX report writing

---

## Author

**Yang Jiekang**

Project completed in 2026.
