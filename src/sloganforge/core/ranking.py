"""Ranking helpers used by the engine and the refine handler."""

from __future__ import annotations

from sloganforge.models.candidate import SloganCandidate
from sloganforge.utils.scoring import score_candidate


def rerank(candidates: list[SloganCandidate], brief: str, preset) -> list[SloganCandidate]:
    for c in candidates:
        c.score = score_candidate(c.text, brief, preset)
    return sorted(candidates, key=lambda c: c.score, reverse=True)