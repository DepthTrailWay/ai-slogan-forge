"""Batch handler: run many briefs through the engine sequentially.

Used by `slogan-forge batch briefs.txt` and by the GUI when a user drops
a CSV of briefs. Sequential on purpose — hosted backends rate-limit.
"""

from __future__ import annotations

import logging
from pathlib import Path

from sloganforge.core.engine import SloganEngine
from sloganforge.models.candidate import ForgeResult

log = logging.getLogger("sloganforge.handlers.batch")


async def run_batch(engine: SloganEngine, briefs: list[str], count: int = 5) -> list[ForgeResult]:
    results: list[ForgeResult] = []
    for i, brief in enumerate(briefs, start=1):
        log.info("batch %d/%d", i, len(briefs))
        results.append(await engine.forge(brief=brief, count=count))
    return results


def load_briefs(path: Path) -> list[str]:
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]