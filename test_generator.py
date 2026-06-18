from backend.rag.retriever import retrieve
from backend.rag.generator import generate_answer

query = "What are the responsibilities of users regarding security and backup?"

contexts = retrieve(
    query,
    top_k=5
)

answer = generate_answer(
    query,
    contexts
)

print("\nANSWER:\n")
print(answer)