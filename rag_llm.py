# rag_llm.py

from search import search
from config import *
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Load LLM
tokenizer = AutoTokenizer.from_pretrained(LLM_MODEL)
model = AutoModelForCausalLM.from_pretrained(
    LLM_MODEL,
    torch_dtype=torch.float16,
    device_map="auto"
)

def generate_answer(question):
    # 1. Retrieve relevant documents
    docs = search(question)

    # Build context string
    context = "\n\n".join(
        [f"[Doc {i}] {d['title']}\n{d['abstract']}" for i, d in enumerate(docs)]
    )

    prompt = f"""
You are a helpful research assistant.
Answer the user's question based only on the documents below.

Documents:
{context}

Question: {question}

Final Answer (cite using [Doc X]): 
"""

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    output = model.generate(
        **inputs,
        max_new_tokens=300,
        temperature=0.2
    )
    answer = tokenizer.decode(output[0], skip_special_tokens=True)

    return answer
