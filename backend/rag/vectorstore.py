import faiss
import numpy as np
import pickle

def build_faiss(embeddings, chunks):

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(dimension)

    index.add(np.array(embeddings))

    faiss.write_index(
        index,
        "vector_store/faiss.index"
    )

    with open(
        "vector_store/chunks.pkl",
        "wb"
    ) as f:
        pickle.dump(chunks, f)

    return index