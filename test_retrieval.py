from backend.rag.retriever import retrieve

results = retrieve(
    "AWS Security",
    top_k=5
)

for i, chunk in enumerate(results):

    print("\n")
    print("=" * 50)
    print(f"RESULT {i+1}")
    print("=" * 50)

    print(chunk[:1000])