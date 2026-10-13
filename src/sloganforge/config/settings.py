"""Settings loader.

Reads from environment (via python-dotenv) with sane defaults. One
Settings object is built once at startup and passed down.
"""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

from sloganforge.config.presets import DEFAULT_PRESET, Preset

load_dotenv()


@dataclass(frozen=True, slots=True)
class Settings:
    backend: str
    endpoint: str
    api_key: str
    model: str
    timeout_s: float
    temperature: float
    local_model: str
    models_root: str
    context_len: int
    preset: Preset


def load_settings() -> Settings:
    preset_name = os.getenv("SF_PRESET", DEFAULT_PRESET.name)
    from sloganforge.config.presets import PRESETS

    preset = PRESETS.get(preset_name, DEFAULT_PRESET)
    return Settings(
        backend=os.getenv("SF_BACKEND", "hosted"),
        endpoint=os.getenv("SF_ENDPOINT", "https://api.openai.com/v1"),
        api_key=os.getenv("SF_API_KEY", ""),
        model=os.getenv("SF_MODEL", "gpt-4o-mini"),
        timeout_s=float(os.getenv("SF_TIMEOUT", "30")),
        temperature=float(os.getenv("SF_TEMPERATURE", "0.95")),
        local_model=os.getenv("SF_LOCAL_MODEL", "models/slogan-7b-q4.gguf"),
        models_root=os.getenv("SF_MODELS_ROOT", "models"),
        context_len=int(os.getenv("SF_CONTEXT", "2048")),
        preset=preset,
    )