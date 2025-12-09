# build_db.py

import sqlite3
import faiss
import numpy as np
import arxiv
from sentence_transformers import SentenceTransformer
from config import *

# 1) Fetch papers from ArXiv
def fetch_papers(query, max_results):
    search = arxiv.Search(query=query, max_results=max_results)
    return list(search.results())

# 2) Create SQLite DB
def setup_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""CREATE TABLE IF NOT EXISTS documents (
        doc_id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        url TEXT,
        abstract TEXT
    )""")

    conn.commit()
    return conn, c

# 3) Insert metadata
def insert_papers(cursor, papers):
    for p in papers:
        cursor.execute(
            "INSERT INTO documents (title, url, abstract) VALUES (?, ?, ?)",
            (p.title, p.entry_id, p.summary)
        )

# 4) Build FAISS index
def build_faiss(embeddings):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    return index

# ---------------- MAIN -----------------

if __name__ == "__main__":
    print("📥 Fetching ArXiv papers...")
    papers = fetch_papers(ARXIV_QUERY, MAX_RESULTS)

    print("🗄 Setting up SQLite DB...")
    conn, c = setup_db()
    insert_papers(c, papers)
    conn.commit()

    print("🧠 Loading embedding model...")
    model = SentenceTransformer(EMBED_MODEL)

    print("📐 Creating embeddings...")
    abstracts = [p.summary for p in papers]
    embeddings = model.encode(abstracts, convert_to_numpy=True).astype("float32")

    print("🔍 Building FAISS index...")
    index = build_faiss(embeddings)
    faiss.write_index(index, FAISS_FILE)

    print("\n✅ Database + FAISS vector store created!")
    print(f"SQLite DB:   {DB_FILE}")
    print(f"FAISS Index: {FAISS_FILE}\n")
