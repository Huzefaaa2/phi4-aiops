from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from pathlib import Path

from aiops_copilot.config import get_settings
from aiops_copilot.integrations.ollama_client import OllamaClient
from aiops_copilot.models import QueryResponse, Remediation
from aiops_copilot.rag.vector_store import LocalVectorStore


class CopilotService:
    def __init__(self) -> None:
        settings = get_settings()
        self.settings = settings
        self.store = LocalVectorStore(settings.vector_index_path, settings.metadata_path)
        self.ollama = OllamaClient(settings.ollama_base_url, settings.ollama_model)

    def ingest_local_logs(self, server: str) -> int:
        logs_dir = Path(self.settings.logs_path) / server
        if not logs_dir.exists():
            return 0

        texts: list[str] = []
        payloads: list[dict] = []
        for file in logs_dir.glob("*.jsonl"):
            for line in file.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                item = json.loads(line)
                text = f"[{item.get('timestamp')}] {item.get('level')} {item.get('source')}#{item.get('event_id')}: {item.get('message')}"
                texts.append(text)
                payloads.append(item)

        if not texts:
            return 0
        return self.store.upsert(texts, payloads)

    def query(self, server: str, question: str, window_hours: int = 24) -> QueryResponse:
        cutoff = datetime.now(tz=timezone.utc) - timedelta(hours=window_hours)
        hits = self.store.search(f"{server} {question}", k=12)

        filtered = [h for h in hits if h.payload.get("server") == server and _to_dt(h.payload.get("timestamp")) >= cutoff]
        evidence = [
            f"{item.payload.get('timestamp')} {item.payload.get('level')} {item.payload.get('source')} -> {item.payload.get('message')}"
            for item in filtered[:8]
        ]

        prompt = (
            "You are an enterprise AIOps copilot. Return JSON with keys: answer, root_cause, confidence, "
            "evidence (array of short strings), suggested_remediation (array of objects title, command, risk).\n\n"
            f"Server: {server}\nQuestion: {question}\n\nRelevant evidence:\n" + "\n".join(evidence)
        )
        generated = self.ollama.generate_json(prompt)

        remediation = [Remediation(**r) for r in generated.get("suggested_remediation", []) if isinstance(r, dict)]
        return QueryResponse(
            answer=generated.get("answer", "No answer generated."),
            root_cause=generated.get("root_cause", "Unknown"),
            confidence=float(generated.get("confidence", 0.2)),
            evidence=generated.get("evidence", evidence),
            suggested_remediation=remediation,
            raw=generated,
        )


def _to_dt(value: str | None) -> datetime:
    if not value:
        return datetime(1970, 1, 1, tzinfo=timezone.utc)
    return datetime.fromisoformat(value.replace("Z", "+00:00"))
