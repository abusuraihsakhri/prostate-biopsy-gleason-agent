# Prostate Biopsy Gleason Agent

> **Domain:** Digital Pathology & Quantitative Histopathology
> **Reference Guidelines & Standards:** College of American Pathologists (CAP) Synoptic Protocols & DICOM WSI

<div align="center">

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111-009688.svg?logo=fastapi&logoColor=white)
![Audit Trail](https://img.shields.io/badge/Audit-HMAC--SHA256_Tamper--Evident-brightgreen.svg)
![Zero-PHI Guard](https://img.shields.io/badge/Guard-Zero--PHI_Outbound-blue.svg)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg?logo=docker&logoColor=white)

</div>

---

## 📖 What It Does

**Prostate Biopsy Gleason Agent** is an advanced analytical and computational platform implementing Multi-Core ISUP Grade Grouping & Perineural Invasion Tracker. It provides autonomous evaluation of prostate biopsy specimens through specialized sub-agents that assess clinical metrics, classify Gleason patterns, and detect biomarker discordance.

---

## ⚙️ Key Capabilities & Algorithmic Modules

### 🔬 Core Algorithmic & Evaluation Engines

- **`prostate_gleason.py`** — Standalone domain pathology engine with Gleason grading and pattern recognition
- **`agents/supervisor.py`** — Enterprise supervisor orchestrating multiple worker evaluations
- **`agents/workers.py`** — Specialized domain workers:
  - `InvariantQCWorker` — Primary metric threshold monitoring
  - `SafetyEscalationWorker` — STAT kinetics & emergency interlock detection
  - `ProtocolConformanceWorker` — Discordance & anomaly triage
- **`agents/base.py`** — PHI guard, HMAC-SHA256 audit trail, and security exceptions
- **`enrichment.py`** — Extended enrichment suite for WHO 2019 compliance, GS7 subtype detection, and pattern 4 tracking

---

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/abusuraihsakhri/prostate-biopsy-gleason-agent.git
cd prostate-biopsy-gleason-agent

# Install dependencies (no required runtime deps for core functionality)
pip install --editable .

# For full features (FastAPI server, Prometheus):
pip install fastapi uvicorn pydantic

# For running tests:
pip install pytest
```

---

## 💻 CLI Quickstart & Usage

### 1. Guided Interactive Mode
```bash
python cli.py audit --task-id CASE-001
```

### 2. Direct Parameterized Evaluation
```bash
python cli.py audit --task-id TASK-001 --target SPECIMEN-01 --primary 28.5 --secondary 14.2 --critical --status DISCORDANT
```

### 3. Batch Processing
```bash
python cli.py batch -i sample.csv -o results.csv
```

### 4. System Chat Assistant
```bash
python cli.py chat "What is the system status?"
```

### 5. Audit Trail Verification
```bash
python cli.py verify-audit
```

### 6. Launch REST API Server
```bash
python cli.py serve --host 127.0.0.1 --port 8000
```

### Parameter Reference
- `--task-id`: Unique task / case identifier
- `--target`: Specimen or entity identifier
- `--primary`: Primary measurement or score (float)
- `--secondary`: Secondary kinetic or confidence score (float)
- `--critical`: Emergency escalation flag (boolean)
- `--status`: Status code or phenotype descriptor

---

## 🛡️ Security & Enterprise Architecture

* **Zero-PHI Outbound Interceptor:** Active regex inspection blocking SSNs, MRNs, phone numbers, and patient identifiers.
* **Tamper-Evident HMAC-SHA256 Audit Trail:** Chained, cryptographically signed logs for every evaluation and state transition.
* **Required Environment Variable:** `AUDIT_SECRET_KEY` must be set before using audit functionality.
* **Air-Gapped LLM Reasoning Adapter:** Agnostic integration for local Ollama instances, Claude 3.5 Sonnet, GPT-4o, and deterministic test mocks.
* **Input Validation:** All metric values validated as finite numbers (rejects NaN, Inf, None).

### Environment Variables

| Variable | Required | Description |
|:---------|:---------|:------------|
| `AUDIT_SECRET_KEY` | Yes | HMAC signing key for audit trail (set before first use) |
| `MODEL_PROVIDER` | No | LLM provider: `mock`, `ollama`, `claude`, `openai` (default: `mock`) |

---

## 🧪 Testing & Verification

```bash
# Run the full test suite (26 tests)
pytest -v

# Run with coverage
pytest -v --cov

# Execute high-throughput batch simulation benchmarks
python simulator.py 1000
```

---

## 🐳 Container Deployment

```bash
# Build and run with Docker Compose (recommended)
docker-compose up --build

# Or build and run manually
docker build -t prostate-biopsy-gleason-agent .
docker run -p 8000:8000 -e AUDIT_SECRET_KEY=your-secret-key prostate-biopsy-gleason-agent
```

---

## 📁 Project Structure

```
prostate-biopsy-gleason-agent/
├── agents/                          # Enterprise supervisor & worker modules
│   ├── __init__.py
│   ├── api.py                       # FastAPI REST endpoints
│   ├── base.py                      # PHI guard, audit trail, security
│   ├── learning.py                  # Bayesian calibration engine
│   ├── llm_factory.py               # LLM provider abstraction
│   ├── metrics.py                   # Prometheus metrics collector
│   ├── models.py                    # Pydantic schemas
│   ├── streamer.py                  # WebSocket telemetry
│   ├── supervisor.py                # Master orchestrator
│   └── workers.py                   # Specialized domain workers
├── prostate_biopsy_gleason_agent/   # Clinical domain package
│   ├── __init__.py
│   ├── agents.py                    # Clinical sub-agents
│   ├── cli.py                       # Clinical CLI
│   ├── engine.py                    # Clinical domain rules
│   ├── models.py                    # Clinical data models
│   └── server.py                    # Clinical FastAPI server
├── tests/                           # Test suite
│   ├── test_enrichment.py           # Enrichment module tests
│   ├── test_prostate_biopsy_gleason_agent.py  # Agent/worker tests
│   └── test_prostate_biopsy_gleason_package.py # Package tests
├── web/
│   └── index.html                   # Operations dashboard
├── cli.py                           # Main CLI entry point
├── prostate_gleason.py              # Standalone domain engine
├── prostate_gleason_app.py          # Domain engine app entry
├── prostate_biopsy_gleason_agent_app.py  # Package app entry
├── enrichment.py                    # Extended enrichment features
├── simulator.py                     # High-throughput simulator
├── pyproject.toml                   # Project configuration
├── Dockerfile                       # Container build
├── docker-compose.yml               # Container orchestration
├── sample.csv                       # Sample batch input
├── sample_payload.json              # Sample API payload
├── benchmark_dataset.json           # Golden benchmark test cases
└── openapi_spec.json                # OpenAPI 3.1 specification
```

---

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) for details.
