"""Text hygiene for briefs before they hit a prompt.

Strips control tokens and the delimiters the prompt builder uses, so a
brief can't close the <brand_brief> block early.
"""

from __future__ import annotations

import re

_CONTROL = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")
_DELIM = re.compile(r"</?brand_brief>", re.IGNORECASE)


def strip_control_tokens(text: str, max_len: int = 2000) -> str:
    cleaned = _CONTROL.sub("", text)
    cleaned = _DELIM.sub("", cleaned)
    return cleaned[:max_len].strip()