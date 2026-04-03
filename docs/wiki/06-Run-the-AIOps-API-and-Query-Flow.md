# 06 - Run the AIOps API and Query Flow

## Start API

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -e .
uvicorn aiops_copilot.main:app --host 0.0.0.0 --port 8000
```

## Ingest Logs

```bash
curl -X POST http://<host>:8000/ingest/<server-name>
```

## Query Server

```bash
curl -X POST http://<host>:8000/query \
  -H "Content-Type: application/json" \
  -d '{"server":"<server-name>","question":"What changed before failure?"}'
```

## Expected Output

- `answer`
- `root_cause`
- `confidence`
- `evidence[]`
- `suggested_remediation[]`

