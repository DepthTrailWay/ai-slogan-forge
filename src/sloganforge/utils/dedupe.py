"""Near-duplicate collapse for slogan candidates.

Exact matches drop first. Then a normalized-key pass (lowercase, strip
punctuation) catches "Just Do It." vs "just do it".
"""

from __future__ import annotations

import re

from sloganforge.models.candidate import SloganCandidate

_PUNCT = re.compile(r"[^\w\s]")


def _norm(text: str) -> str:
    return _PUNCT.sub("", text.lower()).strip()


def dedupe_candidates(candidates: list[SloganCandidate]) -> list[SloganCandidate]:
    seen: set[str] = set()
    out: list[SloganCandidate] = []
    for c in candidates:
        key = _norm(c.text)
        if key and key not in seen:
            seen.add(key)
            out.append(c)
    return out