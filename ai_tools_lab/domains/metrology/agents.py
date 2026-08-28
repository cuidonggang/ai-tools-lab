"""Agents for metrology & measurement inspection (计量检测)."""
from __future__ import annotations

from ...core.agent_base import AgentContext, AgentResult, BaseAgent
from ...core.registry import registry


@registry.register_agent
class MeasurementDataAnalysisAgent(BaseAgent):
    """Analyzes measurement/calibration data and flags out-of-tolerance results."""

    name = "metrology.measurement_analysis"
    description = "对计量/校准数据进行统计分析，识别超差与异常趋势"

    def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError("TODO: implement measurement data analysis logic")


@registry.register_agent
class CalibrationReportAgent(BaseAgent):
    """Generates calibration/inspection reports from raw instrument readings."""

    name = "metrology.calibration_report"
    description = "根据仪器原始读数自动生成计量检测/校准报告"

    def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError("TODO: implement calibration report generation")


@registry.register_agent
class ReportAuditAgent(BaseAgent):
    """Runs the report-audit pipeline (parse -> extract -> rules -> LLM) end to end."""

    name = "metrology.report_audit"
    description = "对计量检测/检定/校准报告进行结构化审核，产出可追溯的审核发现列表"

    def run(self, context: AgentContext) -> AgentResult:
        from .report_audit.audit_service import AuditService

        result = AuditService().audit_file(context.input)
        return AgentResult(output=result, metadata={"summary": result.summary})
