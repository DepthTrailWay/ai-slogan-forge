"""Engine tests against a deterministic mock backend."""

from __future__ import annotations

import pytest

from sloganforge.config.presets import DEFAULT_PRESET
from sloganforge.config.settings import Settings
from sloganforge.core.engine import SloganEngine


class MockBackend:
    def __init__(self, lines: list[str]) -> None:
        self._lines = lines

    async def generate(self, prompt: str, n: int) -> list[str]:
        return self._lines[:n]

    async def aclose(self) -> None:
        return None


def _settings() -> Settings:
    return Settings(
        backend="mock",
        endpoint="",
        api_key="",
        model="",
        timeout_s=1.0,
        temperature=0.9,
        local_model="",
        models_root="models",
        context_len=512,
        preset=DEFAULT_PRESET,
    )


@pytest.mark.asyncio
async def test_forge_ranks_and_dedupes() -> None:
    backend = MockBackend(
        [
            "Brew Bold.",
            "brew bold",
            "Synergy-driven cutting-edge solutions",
            "Cold brew, warm city.",
        ]
    )
    engine = SloganEngine(backend=backend, settings=_settings())
    result = await engine.forge(brief="eco cold brew for commuters", count=5)

    texts = [c.text for c in result.candidates]
    assert "Brew Bold." in texts
    assert "brew bold" not in texts  # deduped
    assert result.candidates[0].score >= result.candidates[-1].score


@pytest.mark.asyncio
async def test_empty_brief_returns_empty() -> None:
    engine = SloganEngine(backend=MockBackend(["x"]), settings=_settings())
    result = await engine.forge(brief="   ", count=5)
    assert result.candidates == []