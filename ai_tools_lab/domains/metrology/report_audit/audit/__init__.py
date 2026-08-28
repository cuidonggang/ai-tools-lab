"""Auditors: each takes an ExtractionResult and returns a list[AuditFinding].

completeness/rule/consistency/calculation are pure Python and require no
network access; llm_auditor is the only one that calls an external model.
"""
