"""Local GGUF backend via llama-cpp-python.

Optional dependency. Path is validated to stay inside the configured
models root — see SECURITY.md.
"""

from __future__ import annotations

import logging
from pathlib import Path

from sloganforge.config.settings import Settings

log = logging.getLogger("sloganforge.services.local")


class LocalBackend:
    def __init__(self, settings: Settings) -> None:
        from llama_cpp import Llama  # type: ignore[import-not-found]

        model_path = Path(settings.local_model).resolve()
        root = Path(settings.models_root).resolve()
        if root not in model_path.parents and model_path != root:
            raise ValueError(f"model path escapes models root: {model_path}")

        self._llm = Llama(model_path=str(model_path), n_ctx=settings.context_len, verbose=False)

    async def generate(self, prompt: str, n: int) -> list[str]:
        out = self._llm(prompt, max_tokens=256, temperature=0.9, stop=["\n\n"])
        text = out["choices"][0]["text"]
        return [line for line in text.splitlines() if line.strip()]

    async def aclose(self) -> None:
        self._llm = None