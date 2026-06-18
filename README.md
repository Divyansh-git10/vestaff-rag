# AWS Customer Agreement RAG Assistant

## Overview

This project is a Retrieval-Augmented Generation (RAG) system built on top of the AWS Customer Agreement document.

The application allows users to ask natural language questions about the agreement and receive grounded answers generated from relevant document sections.

The system combines semantic search using FAISS and Sentence Transformers with Large Language Model (LLM) generation using Groq.

---

## Features

* PDF document parsing
* Text chunking and preprocessing
* Semantic embeddings using Sentence Transformers
* FAISS vector database for similarity search
* Context-aware answer generation using Groq LLM
* FastAPI backend
* SQLite query logging
* Analytics endpoint
* Streamlit user interface
* Swagger API documentation

---

## Architecture

AWS Customer Agreement PDF
↓
Document Parser
↓
Text Chunking
↓
Sentence Transformer Embeddings
↓
FAISS Vector Store
↓
Retriever
↓
Groq LLM
↓
Generated Answer

---

## Tech Stack

### Backend

* Python
* FastAPI
* SQLAlchemy
* SQLite

### RAG Components

* Sentence Transformers
* FAISS
* PyPDF

### LLM

* Groq API

### Frontend

* Streamlit

---

## Project Structure

```text
vestaff-rag/
│
├── backend/
│   ├── database/
│   ├── rag/
│   ├── main.py
│   ├── schemas.py
│   └── init_db.py
│
├── frontend/
│   └── app.py
│
├── data/
│   └── AWS Customer Agreement.pdf
│
├── vector_store/
│   ├── faiss.index
│   └── chunks.pkl
│
├── test_ingest.py
├── test_retrieval.py
├── test_generator.py
├── requirements.txt
└── README.md
```

## Setup Instructions

### 1. Clone Repository

```bash
git clone <repo-url>
cd vestaff-rag
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key
```

### 5. Create Database

```bash
python backend/init_db.py
```

### 6. Generate Embeddings and FAISS Index

```bash
python test_ingest.py
```

### 7. Start FastAPI

```bash
uvicorn backend.main:app --reload
```

Swagger:

```text
http://127.0.0.1:8000/docs
```

### 8. Start Streamlit Frontend

```bash
python -m streamlit run frontend/app.py
```

---

## API Endpoints

### POST /ask

Accepts a natural language query and returns:

* Generated answer
* Retrieved source context
* Response latency

### GET /analytics

Returns:

* Total queries
* Unanswered queries
* Average latency

---

## Example Questions

* What are the responsibilities of users regarding security and backup?
* What is AWS indemnification policy?
* Can AWS modify the agreement?
* What are the payment obligations?

---

## Analytics

The system logs every query in SQLite and tracks:

* Query count
* Answer success rate
* Average response latency

---

## Future Improvements

* Hybrid Retrieval (BM25 + FAISS)
* Reranking Layer
* Multi-document support
* Conversation Memory
* Docker Deployment
