"""A deterministic, no-network LLMProvider used for tests and local dry runs."""
from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class FakeLLMProvider:
    """Returns a pre-canned JSON response regardless of prompt content."""

    response: str = field(default_factory=lambda: json.dumps({"findings": []}))

    def complete(self, prompt: str, **kwargs: object) -> str:
        return self.response
