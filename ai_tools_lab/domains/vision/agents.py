"""Agents for visual/vision-based inspection (视觉检测)."""
from __future__ import annotations

from ...core.agent_base import AgentContext, AgentResult, BaseAgent
from ...core.registry import registry


@registry.register_agent
class DefectDetectionAgent(BaseAgent):
    """Detects surface/appearance defects from inspection images."""

    name = "vision.defect_detection"
    description = "基于视觉模型检测产品表面/外观缺陷"

    def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError("TODO: implement defect detection logic")


@registry.register_agent
class DimensionMeasurementAgent(BaseAgent):
    """Measures dimensional features from calibrated images."""

    name = "vision.dimension_measurement"
    description = "基于标定图像进行尺寸/几何特征测量"

    def run(self, context: AgentContext) -> AgentResult:
        raise NotImplementedError("TODO: implement vision-based dimension measurement")
