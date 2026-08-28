"""Report Audit: intelligent audit pipeline for metrology inspection/calibration reports.

Pipeline: ingestion -> extraction -> rule/consistency/calculation auditors -> LLM
semantic auditor -> aggregation. See models/, ingestion/, extraction/, rules/,
audit/, llm/ and audit_service.py for the individual stages.
"""
