import faiss
import pickle
import numpy as np

from .embeddings import model

index = faiss.read_index("vector_store/faiss.index")

with open("vector_store/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

def retrieve(query, top_k=5):

    q_emb = model.encode([query])

    distances, indices = index.search(
        np.array(q_emb),
        top_k
    )


    results = []

    for idx in indices[0]:
        results.append(chunks[idx])

    return results