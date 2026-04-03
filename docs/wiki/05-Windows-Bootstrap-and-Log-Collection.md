# 05 - Windows Bootstrap and Log Collection

## Bootstrap Script

Use `scripts/windows/bootstrap-aiops.ps1` to:
- Install runtime dependencies
- Create Python venv
- Start Ollama and pull model
- Register scheduled collector task

```powershell
powershell -ExecutionPolicy Bypass -File C:\Phi4AIOps\bootstrap-aiops.ps1 -OllamaModel "phi4:mini"
```

## Log Collector Script

`collect-events.ps1` exports recent events to JSONL for ingestion.

```powershell
powershell -ExecutionPolicy Bypass -File C:\Phi4AIOps\collect-events.ps1 -LookbackMinutes 60
```

## Validation

- Confirm output folder exists
- Confirm `.jsonl` files are generated
- Confirm scheduled task runs every 15 minutes

