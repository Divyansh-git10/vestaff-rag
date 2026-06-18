from backend.rag.parser import extract_text
from backend.rag.chunker import chunk_text
from backend.rag.embeddings import get_embeddings
from backend.rag.vectorstore import build_faiss

pdf_path = "data/AWS Customer Agreement.pdf"

print("Extracting PDF...")

text = extract_text(pdf_path)

print("Text length:", len(text))

chunks = chunk_text(text)

print("Chunks:", len(chunks))

embeddings = get_embeddings(chunks)

print("Embedding shape:", embeddings.shape)

build_faiss(
    embeddings,
    chunks
)

print("FAISS Index Created Successfully")