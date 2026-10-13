"""Heuristic scorer for slogan candidates.

Not a taste oracle — a filter. Rewards brevity, penalizes clichés and
over-length, gives a small bump for concrete nouns from the brief.
"""

from __future__ import annotations

import re

from sloganforge.config.presets import Preset

_CLICHE = {
    "synergy", "leverage", "best-in-class", "world-class", "cutting-edge",
    "next-generation", "game-changer", "seamless", "robust", "innovative",
}
_WORD = re.compile(r"[a-z']+")


def score_candidate(text: str, brief: str, preset: Preset) -> float:
    words = _WORD.findall(text.lower())
    if not words:
        return 0.0

    score = 60.0

    # Length: sweet spot 3-9 words.
    n = len(words)
    if 3 <= n <= 9:
        score += 12.0
    elif n < 3:
        score -= 8.0
    else:
        score -= (n - 9) * 2.5

    # Cliché penalty.
    if any(w in _CLICHE for w in words):
        score -= 18.0

    # Brief overlap bump.
    brief_words = set(_WORD.findall(brief.lower()))
    overlap = len(set(words) & brief_words)
    score += min(overlap * 3.0, 12.0)

    # Preset weight nudge.
    score += preset.score_bias

    return max(0.0, min(100.0, score))