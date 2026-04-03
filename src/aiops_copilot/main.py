from fastapi import FastAPI, HTTPException

from aiops_copilot.models import QueryRequest, QueryResponse
from aiops_copilot.service import CopilotService

app = FastAPI(title="Phi-4 AIOps Copilot", version="0.1.0")
service = CopilotService()


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/ingest/{server}")
def ingest(server: str) -> dict:
    ingested = service.ingest_local_logs(server)
    return {"server": server, "ingested": ingested}


@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest) -> QueryResponse:
    if not request.question.strip():
        raise HTTPException(status_code=400, detail="Question is required")
    return service.query(request.server, request.question, request.window_hours)
