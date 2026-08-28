"""Loads global and per-domain YAML configuration files from configs/."""
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

CONFIG_DIR = Path(__file__).resolve().parents[2] / "configs"


def load_yaml(relative_path: str) -> dict[str, Any]:
    """Load a YAML file located under the configs/ directory."""
    path = CONFIG_DIR / relative_path
    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_settings() -> dict[str, Any]:
    """Load the global settings.yaml (LLM provider, logging, ...)."""
    return load_yaml("settings.yaml")


def load_domain_config(domain: str) -> dict[str, Any]:
    """Load configs/agents/<domain>.yaml (enabled agents for that domain)."""
    return load_yaml(f"agents/{domain}.yaml")
