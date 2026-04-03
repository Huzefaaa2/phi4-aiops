from __future__ import annotations

import os
import httpx
from botbuilder.core import ActivityHandler, TurnContext


class AiOpsTeamsBot(ActivityHandler):
    async def on_message_activity(self, turn_context: TurnContext):
        text = (turn_context.activity.text or "").strip()
        if not text.startswith("@"):  # Require explicit server mention e.g. @win-az-01 what changed?
            await turn_context.send_activity("Reference a server using @server-name followed by your question.")
            return

        parts = text.split(maxsplit=1)
        server = parts[0].lstrip("@").lower()
        question = parts[1] if len(parts) > 1 else "Summarize latest anomalies"

        api_url = os.getenv("AIOPS_API_URL", "http://localhost:8000/query")
        payload = {"server": server, "question": question, "window_hours": 24}

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(api_url, json=payload)
            response.raise_for_status()
            data = response.json()

        message = (
            f"**Server:** `{server}`\n"
            f"**Root cause:** {data.get('root_cause')}\n"
            f"**Confidence:** {data.get('confidence')}\n"
            f"**Answer:** {data.get('answer')}\n"
        )
        await turn_context.send_activity(message)
