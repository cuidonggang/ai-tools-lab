"""Command-line entry point: `python -m ai_tools_lab.domains.metrology.report_audit <file>`."""
from __future__ import annotations

import argparse
import json

from ai_tools_lab.domains.metrology.report_audit.audit_service import AuditService


def main() -> None:
    parser = argparse.ArgumentParser(description="计量检测报告智能审核（MVP，规则+一致性+计算，LLM 语义审核暂未接入 CLI）")
    parser.add_argument("report_path", help="待审核的报告文件路径（.pdf / .docx / .txt）")
    args = parser.parse_args()

    result = AuditService().audit_file(args.report_path)
    output = {
        "summary": result.summary,
        "findings": json.loads(result.model_dump_json())["findings"],
    }
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
