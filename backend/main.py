from fastapi import FastAPI, HTTPException
from time import time
from backend.database.db import SessionLocal
from backend.database.models import QueryLog
from sqlalchemy import func

from backend.schemas import (
    QueryRequest,
    QueryResponse
)

from backend.rag.retriever import retrieve
from backend.rag.generator import generate_answer

app = FastAPI(
    title="Vestaff RAG API"
)

@app.get("/")
def home():

    return {
        "message": "Vestaff RAG API Running"
    }
@app.post("/ask", response_model=QueryResponse)
def ask_question(request: QueryRequest):

    if not request.query.strip():

        raise HTTPException(
            status_code=400,
            detail="Query cannot be empty"
        )

    start_time = time()

    contexts = retrieve(
        request.query,
        top_k=5
    )

    answer = generate_answer(
        request.query,
        contexts
    )

    latency = (
        time() - start_time
    ) * 1000

    db = SessionLocal()

    log = QueryLog(
        query=request.query,
        answer=answer,
        source_chunk=contexts[0],
        latency_ms=latency,
        answer_found=(
            "not available in the document"
            not in answer.lower()
        )
    )

    db.add(log)

    db.commit()

    db.close()

    return {
        "answer": answer,
        "source": contexts[0][:500],
        "latency_ms": round(
            latency,
            2
        )
    }
@app.get("/analytics")
def analytics():

    db = SessionLocal()

    total_queries = db.query(QueryLog).count()

    unanswered_queries = (
        db.query(QueryLog)
        .filter(QueryLog.answer_found == False)
        .count()
    )

    avg_latency = (
        db.query(
            func.avg(QueryLog.latency_ms)
        )
        .scalar()
    )

    most_frequent = (
        db.query(
            QueryLog.query,
            func.count(QueryLog.query).label("count")
        )
        .group_by(QueryLog.query)
        .order_by(
            func.count(QueryLog.query).desc()
        )
        .limit(5)
        .all()
    )

    db.close()

    return {
        "total_queries": total_queries,
        "unanswered_queries": unanswered_queries,
        "average_latency_ms": round(
            avg_latency or 0,
            2
        ),
        "most_frequent_questions": [
            {
                "query": q,
                "count": c
            }
            for q, c in most_frequent
        ]
    }
@app.post("/ingest")
def ingest_document():

    from backend.rag.parser import extract_text
    from backend.rag.chunker import chunk_text
    from backend.rag.embeddings import get_embeddings
    from backend.rag.vectorstore import build_faiss

    text = extract_text(
        "data/AWS Customer Agreement.pdf"
    )

    chunks = chunk_text(text)

    embeddings = get_embeddings(
        chunks
    )

    build_faiss(
        embeddings,
        chunks
    )

    return {
        "message": "Document ingested successfully",
        "chunks_created": len(chunks)
    }