from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()

class QueryLog(Base):

    __tablename__ = "query_logs"

    id = Column(Integer, primary_key=True)

    query = Column(String)

    answer = Column(String)

    source_chunk = Column(String)

    latency_ms = Column(Float)

    answer_found = Column(Boolean)