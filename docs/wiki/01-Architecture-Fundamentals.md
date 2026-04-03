# 01 - Architecture Fundamentals

## Core Concept

Phi-4 AIOps Copilot is a **local-first operations reasoning layer**. Logs stay near your workload while the model provides contextual diagnostics.

## Main Components

- **Windows VM** (Azure or VMware)
- **Collector** (`collect-events.ps1`) exporting JSONL logs
- **AIOps API** (`FastAPI`) for ingest/query
- **RAG Layer** (`FAISS` + embeddings)
- **Model Runtime** (`Ollama` + Phi-4)
- **Ops Interface** (Teams bot pattern)

## Data Flow (Simple)

1. Windows events are exported regularly.
2. API ingests and vectorizes log records.
3. Query retrieves most relevant evidence.
4. Phi-4 synthesizes probable root cause + remediation.
5. Output is returned in structured JSON and human-readable text.

## Why This Pattern Matters

- Privacy: no mandatory external log upload
- Latency: local reasoning path
- Cost: small model efficiency
- Control: governance and approvals remain internal

