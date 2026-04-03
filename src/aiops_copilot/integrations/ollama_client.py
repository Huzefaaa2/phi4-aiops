from __future__ import annotations

import json
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential


class OllamaClient:
    def __init__(self, base_url: str, model: str) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=8))
    def generate_json(self, prompt: str) -> dict:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json",
        }

        with httpx.Client(timeout=60.0) as client:
            r = client.post(f"{self.base_url}/api/generate", json=payload)
            r.raise_for_status()
            data = r.json()
            response = data.get("response", "{}")
            if isinstance(response, dict):
                return response
            try:
                parsed = json.loads(response)
                if isinstance(parsed, dict):
                    return parsed
            except json.JSONDecodeError:
                pass
            return {
                "answer": str(response),
                "root_cause": "Unknown",
                "confidence": 0.2,
                "evidence": [],
                "suggested_remediation": [],
            }
