"""Refine handler: take a chosen slogan and push it in a direction.

"Make it punchier", "shorter", "more premium" — each refine is one extra
backend call with the original slogan pinned in the prompt.
"""

from __future__ import annotations

from sloganforge.core.engine import SloganEngine
from sloganforge.models.candidate import ForgeResult


async def refine(
    engine: SloganEngine,
    original: str,
    direction: str,
    count: int = 6,
) -> ForgeResult:
    brief = f'Refine this slogan: "{original}". Direction: {direction}.'
    return await engine.forge(brief=brief, count=count)