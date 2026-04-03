# 09 - Production Hardening Checklist

## Security

- [ ] mTLS or private networking for API
- [ ] Secret management via vault/KMS
- [ ] RBAC for query and remediation actions
- [ ] Script signing policy for PowerShell

## Reliability

- [ ] Health checks and restart policies
- [ ] Scheduled backup of index + metadata
- [ ] Monitoring on ingestion lag and query latency

## Governance

- [ ] Audit trail for queries and responses
- [ ] Human approval for high-risk remediation
- [ ] Data retention policy and PII controls

## Operations

- [ ] Runbooks for degraded model service
- [ ] Change management integration
- [ ] Shift handover summaries

