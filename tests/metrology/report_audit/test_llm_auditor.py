"""Tests LLMAuditor's structured-output validation and evidence verification using a fake provider."""
from __future__ import annotations

import json

from ai_tools_lab.domains.metrology.report_audit.audit.llm_auditor import LLMAuditor
from ai_tools_lab.domains.metrology.report_audit.extraction.result import ExtractionResult
from ai_tools_lab.domains.metrology.report_audit.llm.fake_provider import FakeLLMProvider
from ai_tools_lab.domains.metrology.report_audit.models.raw_document import RawDocument, RawPage
from ai_tools_lab.domains.metrology.report_audit.models.report import Report


def _extraction(text: str) -> ExtractionResult:
    raw_document = RawDocument(source_path="test", file_hash="x", pages=[RawPage(index=0, text=text)])
    return ExtractionResult(report=Report(), raw_document=raw_document, field_occurrences={})


def test_valid_finding_with_verifiable_evidence_is_kept() -> None:
    extraction = _extraction("校准点为 0、10、20、30，量程为 0~100 MPa")
    response = {
        "findings": [
            {
                "category": "semantic",
                "severity": "warning",
                "title": "校准点未覆盖完整量程",
                "description": "校准点集中在低量程区间",
                "evidence_excerpts": ["校准点为 0、10、20、30"],
                "confidence": 0.8,
                "suggestion": "建议增加高量程校准点",
                "insufficient_evidence": False,
            }
        ]
    }
    provider = FakeLLMProvider(response=json.dumps(response, ensure_ascii=False))
    auditor = LLMAuditor(provider)

    findings = auditor.audit(extraction, existing_findings=[])

    assert len(findings) == 1
    assert findings[0].evidence[0].excerpt == "校准点为 0、10、20、30"
    assert auditor.last_status == "ok"


def test_evidence_not_found_in_source_lowers_confidence() -> None:
    extraction = _extraction("报告正文完全不包含下面这句话")
    response = {
        "findings": [
            {
                "category": "semantic",
                "severity": "warning",
                "title": "疑似问题",
                "description": "d",
                "evidence_excerpts": ["这句话在原文中并不存在"],
                "confidence": 0.9,
                "insufficient_evidence": False,
            }
        ]
    }
    provider = FakeLLMProvider(response=json.dumps(response, ensure_ascii=False))
    findings = LLMAuditor(provider).audit(extraction, existing_findings=[])
    assert findings[0].evidence == []
    assert findings[0].confidence <= 0.3


def test_insufficient_evidence_produces_no_finding() -> None:
    extraction = _extraction("报告正文")
    response = {
        "findings": [
            {
                "category": "semantic",
                "severity": "info",
                "title": "无法判断",
                "description": "证据不足",
                "evidence_excerpts": [],
                "confidence": 0.1,
                "insufficient_evidence": True,
            }
        ]
    }
    provider = FakeLLMProvider(response=json.dumps(response, ensure_ascii=False))
    findings = LLMAuditor(provider).audit(extraction, existing_findings=[])
    assert findings == []


def test_invalid_json_exhausts_retries_and_returns_no_findings() -> None:
    provider = FakeLLMProvider(response="not json")
    auditor = LLMAuditor(provider, max_retries=1)
    findings = auditor.audit(_extraction("x"), existing_findings=[])
    assert findings == []
    assert auditor.last_status == "failed"
