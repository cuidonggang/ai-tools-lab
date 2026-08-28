"""Thin, provider-agnostic wrapper around LLM calls used by agents."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Protocol


class LLMProvider(Protocol):
    """Interface any concrete LLM backend (OpenAI, Azure OpenAI, local, ...) must satisfy."""

    def complete(self, prompt: str, **kwargs: Any) -> str:
        ...


@dataclass
class LLMClient:
    """Delegates completion requests to a configured provider implementation."""

    provider: LLMProvider

    def complete(self, prompt: str, **kwargs: Any) -> str:
        return self.provider.complete(prompt, **kwargs)
