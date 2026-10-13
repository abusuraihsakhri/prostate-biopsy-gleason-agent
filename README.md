# Prostate Biopsy Gleason Agent

A Python demonstration of multi-agent threshold auditing, with a separate deterministic **Gleason score / ISUP Grade Group lookup** for *pathologist-assigned* primary and secondary prostate biopsy patterns. It is **not** an image-analysis system, autonomous pathology grader, clinically validated diagnostic device, or HIPAA-compliant clinical platform.

## Browser application

The repository-root `index.html` provides a standalone Grade Group lookup that runs entirely in the browser using `web/grading.js`. Select primary and secondary Gleason patterns (3, 4, or 5), then calculate the score and ISUP Grade Group. No server, cookies, browser storage, analytics, or file upload is required. The browser UI does not process patient data.

GitHub Pages deployment is defined in `.github/workflows/pages.yml`; publication requires GitHub Pages to be enabled for GitHub Actions and a successful deployment. A live link is intentionally not claimed until verified.

## Python installation and use

Requires Python 3.10–3.12 (the CI test matrix). From the repository root:

```bash
python -m pip install -e .
prostate-biopsy-gleason-engine grade 3 4
python -m pytest -q
```

The `grade` command returns the Gleason score and Grade Group; `prostate_biopsy_gleason_agent.grading.grade_group(3, 4)` offers the same deterministic lookup in Python. A 3+4=7 result corresponds to Grade Group 2; 4+3=7 corresponds to Grade Group 3. Gleason 8 (4+4, 3+5, 5+3) corresponds to Group 4; Gleason 9–10 to Group 5.

### Legacy demonstration workflows

The repository also preserves separate, generic numeric-threshold audit implementations. **These are operational examples, not accepted prostate-biopsy grading criteria.** They do not derive Gleason patterns from core lengths, tumour percentages, or histology images.

```bash
python cli.py audit --task-id DEMO-001 --target SPECIMEN-001 --primary 28 --secondary 14
python cli.py batch -i your_generic_tasks.csv -o results.csv
python -m prostate_biopsy_gleason_agent.cli grade 3 4
```

The root `cli.py` uses the Pydantic worker supervisor. The installable console command uses the clinical-package interface. The legacy `web/index.html` console requires a compatible local REST backend; if it is unavailable, it reports an error instead of fabricating results.

## Local REST server and container

Install optional server dependencies:

```bash
python -m pip install fastapi uvicorn pydantic
export AUDIT_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
python cli.py serve --host 127.0.0.1 --port 8000
```

The root server exposes `/health`, `/api/audit`, and `/api/chat` for demonstration use. For Docker, define a strong `AUDIT_SECRET_KEY` in your environment and run `docker compose up --build`. The Compose port binds to **127.0.0.1:8000** by default. Do not expose this unauthenticated demonstration API to untrusted networks.

## Privacy and security limits

- Use **synthetic data only**. The rule-based identifier scanner is incomplete and is not a substitute for de-identification or HIPAA Safe Harbor compliance.
- The HMAC-SHA256 in-memory audit log requires `AUDIT_SECRET_KEY` and verifies individual signatures and predecessor links. It is **not** durable across restarts, an external immutable audit ledger, or a compliance certification.
- The committed historic Docker signing values must be regarded as compromised and **must never be reused**.
- The default language-model adapter is a local deterministic mock. Selecting another provider currently does not connect to an external model.
- Inputs are not used for clinical decision-making, treatment recommendations, or automated notifications.

## Tests and deployment

```bash
python -m pip install -e . fastapi uvicorn pydantic pytest
python -m pytest -q
node web/test_grading.cjs
```

GitHub Actions tests Python 3.10, 3.11, 3.12, the browser lookup, and a signed-audit self-check. The static GitHub Pages workflow deploys only `index.html` and `web/grading.js` and does **not** deploy FastAPI or expose server-side secrets. No Pyodide/PyScript runtime is necessary because the browser calculation is implemented directly in JavaScript.

## References and license

- [EAU prostate cancer classification, staging and ISUP grade groups](https://uroweb.org/guidelines/prostate-cancer/chapter/classification-and-staging-systems)
- [College of American Pathologists prostate needle biopsy protocols](https://www.cap.org/protocols-and-guidelines/cancer-protocols/current-cancer-protocols/)

MIT License — see [LICENSE](LICENSE).
