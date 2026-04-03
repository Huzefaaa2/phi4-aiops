# 07 - Teams Integration Guide

## Goal

Allow operators to query with `@server-name` and receive incident reasoning in Teams.

## Integration Flow

1. Teams message received
2. Bot extracts server mention + question
3. Bot calls `/query`
4. Bot returns summary to chat

## Environment Variable

```env
AIOPS_API_URL=http://<api-host>:8000/query
```

## Message Example

```text
@win-az-aiops-01 Compare last failed backup with last successful run.
```

