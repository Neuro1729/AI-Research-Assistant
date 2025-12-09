# search.py

import sqlite3
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
from config import *

# Load DB
conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Load FAISS
index = faiss.read_index(FAISS_FILE)

# Load embedding model
model = SentenceTransformer(EMBED_MODEL)

def search(query, top_k=TOP_K):
    # Embed query
    q_vec = model.encode([query], convert_to_numpy=True).astype("float32")

    # FAISS search
    distances, indices = index.search(q_vec, top_k)

    results = []
    for i in indices[0]:
        doc = cursor.execute("SELECT title, url, abstract FROM documents WHERE doc_id = ?", (i+1,)).fetchone()
        title, url, abstract = doc
        results.append({
            "title": title,
            "url": url,
            "abstract": abstract
        })

    return results

# CLI usage
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python search.py \"your query here\"")
        exit()

    query = sys.argv[1]
    print(f"\n🔍 Searching for: {query}\n")

    hits = search(query)

    for idx, h in enumerate(hits):
        print(f"--- Result {idx + 1} ---")
        print(f"Title: {h['title']}")
        print(f"URL: {h['url']}")
        print(f"Abstract: {h['abstract'][:300]}...")
        print()
