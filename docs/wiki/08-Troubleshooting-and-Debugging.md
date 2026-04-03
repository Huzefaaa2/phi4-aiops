# 08 - Troubleshooting and Debugging

## Common Issues

### 1) No logs ingested
- Ensure collector output path is correct
- Check file permissions
- Verify JSONL format

### 2) Model timeout
- Confirm Ollama service is running
- Test `OLLAMA_BASE_URL`
- Reduce prompt size / evidence count

### 3) Empty retrieval results
- Confirm ingest endpoint was run
- Check index paths in environment
- Rebuild local index

### 4) Teams bot errors
- Validate `AIOPS_API_URL`
- Confirm bot identity/endpoint configuration

## Useful Commands

```bash
python -m compileall src
```

