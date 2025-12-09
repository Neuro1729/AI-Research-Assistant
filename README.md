# 🧠 ArXiv-RAG

A mini research assistant that retrieves relevant ArXiv papers using **FAISS semantic search** and answers using an **LLM**.

---

## ✨ Features

* Fetches research papers from **ArXiv API**
* Stores metadata in **SQLite**
* Creates embeddings using **SentenceTransformers**
* Builds a **FAISS vector index**
* Performs **semantic search** over abstracts
* Uses an **LLM** (Qwen / Llama) to generate final answers with citations
* Exposes a **FastAPI** endpoint `/ask`

---

## 📂 Project Structure

```
project/
│
├── config.py
├── build_db.py
├── search.py
├── rag_llm.py
├── api.py
└── README.md
```

---

## 📦 Installation

Install required dependencies:

```bash
pip install faiss-cpu sqlite3 arxiv sentence-transformers transformers accelerate fastapi uvicorn
```

---

## ⚙️ Configuration

Edit your `config.py`:

```python
ARXIV_QUERY = "machine learning"
MAX_RESULTS = 40

DB_FILE = "arxiv.db"
FAISS_FILE = "arxiv.index"

EMBED_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
LLM_MODEL = "Qwen/Qwen2.5-0.5B"

TOP_K = 5
```

---

# 🏗️ 1️⃣ Build the Database + Vector Store

Run:

```bash
python build_db.py
```

This will:

* fetch ArXiv papers
* store them in `arxiv.db`
* create embeddings
* build FAISS index `arxiv.index`

You should see:

```
Database + FAISS vector store created!
```

---

# 🔍 2️⃣ Test Semantic Search

Query papers using CLI:

```bash
python search.py "graph neural networks"
```

Example output:

```
--- Result 1 ---
Title: Graph Neural Networks: A Review
URL: https://arxiv.org/abs/xxxx.xxxx
Abstract: Graph neural networks have emerged...

--- Result 2 ---
...
```

---

# 🤖 3️⃣ Test the LLM RAG Answer

Run:

```bash
python - <<EOF
from rag_llm import generate_answer
print(generate_answer("What is a transformer model?"))
EOF
```

You will get an AI-generated answer with citations like:

```
Transformers are neural network architectures [Doc 0][Doc 2].
```

---

# 🚀 4️⃣ Run the FastAPI Server

Start the server:

```bash
uvicorn api:app --reload
```

* `--reload` auto-reloads when code changes
* Server runs at:

```
http://127.0.0.1:8000
```

---

# 🌐 5️⃣ Query the API

Use browser or curl:

```bash
http://127.0.0.1:8000/ask?q=What+is+diffusion+model
```

Example JSON response:

```json
{
  "question": "What is a diffusion model?",
  "answer": "A diffusion model is a generative model that learns to denoise inputs [Doc 1][Doc 3]."
}
```

---

# 🧩 Summary

This project gives you:

✔ ArXiv ingestion
✔ SQLite metadata storage
✔ FAISS vector search
✔ Semantic search CLI
✔ RAG answer generation
✔ FastAPI backend

