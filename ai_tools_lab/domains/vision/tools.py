"""Tools used by visual inspection agents (视觉检测)."""
from __future__ import annotations

from typing import Any

from ...core.registry import registry
from ...core.tool_base import BaseTool


@registry.register_tool
class ImagePreprocessTool(BaseTool):
    """Applies standard preprocessing (resize/normalize) before model inference."""

    name = "vision.image_preprocess"
    description = "对检测图像进行统一预处理（缩放、归一化等）"

    def execute(self, image_path: str, **kwargs: Any) -> str:
        raise NotImplementedError("TODO: implement image preprocessing pipeline")
