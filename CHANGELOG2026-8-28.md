# CHANGELOG 2026-08-28

**Commit**: `2e50df5951f97cca0c6586ba6b1cba10e34d41c8`
**Author**: Donggang Cui <98146972+cuidonggang@users.noreply.github.com>
**Branch**: `main` (pushed to `origin/main`, `803b381..2e50df5`)
**Subject**: Add AI tools lab framework and metrology report audit MVP

## Summary

79 files changed, 2306 insertions(+), 3 deletions(-)

### 1. Resource architecture rebuild

- Replaced the single-file `app.py` skeleton with the `ai_tools_lab/` package: a general Agent/Tool framework for building domain-specific AI tools.
- `core/`: `BaseAgent`, `BaseTool`, global `Registry` (decorator-based registration), YAML config loader, pluggable `LLMProvider` protocol.
- `domains/{metrology,engineering,vision}/`: agent/tool skeletons per business domain.
- `configs/settings.yaml` + `configs/agents/*.yaml`: global and per-domain config.
- `app.py` rewritten as a CLI entry point with `--list-tools`.

### 2. Metrology report intelligent audit (report_audit) MVP

New subsystem under `ai_tools_lab/domains/metrology/report_audit/`:

- `models/`: `Report`, `AuditFinding`, `AuditResult`, `RawDocument`, `SourceLocator` (Pydantic).
- `ingestion/`: PDF (pdfplumber) / Word (python-docx) / plain-text parsers, unified `document_loader`.
- `extraction/`: field/column alias mapping, report and table extraction.
- `rules/`: rule engine + `rules.yaml` (required fields, date rules, etc).
- `audit/`: `completeness_auditor`, `rule_auditor`, `consistency_auditor`, `calculation_auditor`, `llm_auditor`, `aggregator`.
- `llm/`: prompt templates, structured-output validation (evidence substring verification to guard against hallucination), `FakeLLMProvider` for tests.
- `audit_service.py` / `cli.py`: orchestrates the full pipeline; runnable via `python -m ai_tools_lab.domains.metrology.report_audit.cli <file>`.
- `ReportAuditAgent` registered as `metrology.report_audit`, visible via `app.py --list-tools`.

### 3. Tests and verification

- Added 28 tests covering models, parsers, extraction, rule engine, the four deterministic auditors, LLM auditor anti-hallucination logic, end-to-end pipeline, and agent integration. `pytest -q` -> 28 passed.
- Fixed `datetime.utcnow()` deprecation warning -> `datetime.now(UTC)`.
- New dependencies added to `requirements.txt`: `pydantic`, `pdfplumber`, `python-docx`.

### 4. Git operations

- Local commit diverged from `origin/main` (which had several README-only rewrites); rebased cleanly (no conflicts, since this change does not touch README.md), then pushed to `origin/main`.
- Remote reported repository move to `https://github.com/cuidonggang/ai-tools-lab.git` (origin URL not yet updated locally).

Working tree status after this change: clean.
