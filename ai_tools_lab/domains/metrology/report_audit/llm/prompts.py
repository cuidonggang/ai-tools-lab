"""Builds the prompt for the LLM semantic auditor.

The model only ever sees the structured Report + the document's text (not
raw binary/layout) plus the findings already raised by deterministic
auditors, so it can focus on issues rules can't catch instead of repeating
them or free-associating over an unstructured PDF dump.
"""
from __future__ import annotations

import json

from ai_tools_lab.domains.metrology.report_audit.models.finding import AuditFinding
from ai_tools_lab.domains.metrology.report_audit.models.report import Report

_SYSTEM_INSTRUCTIONS = """\
你是计量检测/校准报告的辅助审核员。你只能依据下方提供的结构化数据和原文片段进行判断，
禁止编造报告中不存在的信息。每一条发现都必须在 evidence_excerpts 中给出可以在原文片段中
逐字找到的引用；如果证据不足以下结论，请将该条目标记 insufficient_evidence=true，而不是
猜测。你不需要重复 existing_findings 中已经出现的问题。请只输出符合给定 JSON Schema 的
JSON，不要输出任何其他文字。
"""


def build_semantic_audit_prompt(
    report: Report, source_excerpt: str, existing_findings: list[AuditFinding]
) -> str:
    payload = {
        "report": json.loads(report.model_dump_json()),
        "source_excerpt": source_excerpt,
        "existing_findings": [
            {"category": finding.category.value, "title": finding.title} for finding in existing_findings
        ],
        "output_schema": {
            "findings": [
                {
                    "category": (
                        "completeness|format|consistency|calculation|traceability|"
                        "standard|measurement|uncertainty|conclusion|semantic|compliance"
                    ),
                    "severity": "info|warning|error|critical",
                    "title": "string",
                    "description": "string",
                    "evidence_excerpts": ["原文中可逐字找到的片段"],
                    "confidence": 0.0,
                    "suggestion": "string|null",
                    "insufficient_evidence": False,
                }
            ]
        },
    }
    return _SYSTEM_INSTRUCTIONS + "\n\n" + json.dumps(payload, ensure_ascii=False, indent=2)
