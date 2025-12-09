# api.py

from fastapi import FastAPI
from rag_llm import generate_answer

app = FastAPI()

@app.get("/ask")
def ask(q: str):
    answer = generate_answer(q)
    return {
        "question": q,
        "answer": answer
    }
