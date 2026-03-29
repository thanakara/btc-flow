# ₿
> A production-grade Bitcoin mempool ETL pipeline built with Apache Airflow 3.x, Docker, and Grafana.

---

## Overview

**bitcoin-flow** streams live Bitcoin mempool data from [mempool.space](https://mempool.space) every minute, transforms it into structured records, validates them with Pydantic, and loads them into PostgreSQL — visualized in real-time via a Grafana dashboard.

```
mempool.space API
       │
       ▼
 Airflow DAG (every 1 min)
 ├── extract    → fetch mempool stats + fee estimates
 ├── transform  → flatten & enrich raw data
 ├── validate   → Pydantic model guards bad data
 └── load       → CSV or PostgreSQL (Hydra-driven)
       │
       ▼
 PostgreSQL (btcflow DB)
       │
       ▼
 Grafana Dashboard (auto-refresh 1m)
 ├── Transaction Count over time
 ├── Average Fee Rate over time
 ├── Fee Estimates (fastest / half-hour / hour / economy)
 ├── Latest tx_count (stat)
 └── Total fees in BTC (stat)
```

---

## Stack

| Layer | Technology |
|---|---|
| Orchestration | Apache Airflow 3.x |
| Config | Hydra + OmegaConf |
| Validation | Pydantic v2 |
| Storage | PostgreSQL 15 + CSV |
| Visualization | Grafana 11 |
| Packaging | UV + pyproject.toml |
| Containerization | Docker + Docker Compose |
| Task Runner | Taskfile |
| Testing | pytest |

---
