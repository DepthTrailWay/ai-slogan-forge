"""The forge itself.

Takes a brand brief, builds a prompt, asks a backend for raw candidates,
dedupes, scores, and returns a ranked `ForgeResult`. Backend-agnostic:
anything implementing `SloganBackend` works.
"""

from __future__ import annotations

import logging
from dataclasses import dataclass

from sloganforge.config.settings import Settings
from sloganforge.core.prompt_builder import build_slogan_prompt
from sloganforge.models.candidate import ForgeResult, SloganCandidate
from sloganforge.services.backend import SloganBackend
from sloganforge.utils.dedupe import dedupe_candidates
from sloganforge.utils.scoring import score_candidate

log = logging.getLogger("sloganforge.engine")


@dataclass(slots=True)
class SloganEngine:
    backend: SloganBackend
    settings: Settings

    async def forge(self, brief: str, count: int = 10) -> ForgeResult:
        brief = brief.strip()
        if not brief:
            return ForgeResult(brief="", candidates=[])

        prompt = build_slogan_prompt(brief, self.settings.preset)
        raw = await self.backend.generate(prompt, n=max(count * 3, 24))

        candidates: list[SloganCandidate] = []
        for text in raw:
            cleaned = text.strip().strip('"').strip()
            if not cleaned:
                continue
            candidates.append(
                SloganCandidate(
                    text=cleaned,
                    score=score_candidate(cleaned, brief, self.settings.preset),
                )
            )

        unique = dedupe_candidates(candidates)
        unique.sort(key=lambda c: c.score, reverse=True)
        top = unique[:count]

        log.info("forged %d candidates from %d raw", len(top), len(raw))
        return ForgeResult(brief=brief, candidates=top)