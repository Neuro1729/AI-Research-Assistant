# config.py

ARXIV_QUERY = "machine learning"     # What papers to fetch
MAX_RESULTS = 50                     # How many papers to download

DB_FILE = "arxiv_metadata.db"
FAISS_FILE = "arxiv_faiss.index"

EMBED_MODEL = "all-MiniLM-L6-v2"     # SentenceTransformer model
TOP_K = 5                             # Search K
