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

    db.close()

    return {
        "total_queries": total_queries,
        "unanswered_queries": unanswered_queries,
        "average_latency_ms": round(avg_latency or 0, 2)
    }