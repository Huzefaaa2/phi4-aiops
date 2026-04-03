from datetime import datetime
from pydantic import BaseModel, Field
from typing import Any, List


class LogRecord(BaseModel):
    server: str
    source: str
    level: str
    event_id: int | None = None
    timestamp: datetime
    message: str
    tags: list[str] = Field(default_factory=list)


class QueryRequest(BaseModel):
    server: str
    question: str
    window_hours: int = 24


class Remediation(BaseModel):
    title: str
    command: str
    risk: str


class QueryResponse(BaseModel):
    answer: str
    root_cause: str
    confidence: float
    evidence: List[str]
    suggested_remediation: List[Remediation]
    raw: Any
