"""Prompt construction for slogan generation.

Keeps the brand brief in a delimited block so a malicious brief can't
easily hijack the system instruction. See SECURITY.md.
"""

from __future__ import annotations

from sloganforge.config.presets import Preset
from sloganforge.utils.sanitize import strip_control_tokens

_SYSTEM = (
    "You are a senior brand copywriter. Produce short, memorable slogans "
    "and taglines. One per line. No numbering. No explanations. "
    "Aim for 3-9 words each. Vary rhythm and structure across lines."
)


def build_slogan_prompt(brief: str, preset: Preset) -> str:
    safe_brief = strip_control_tokens(brief)
    tone = preset.tone
    style = preset.style
    return (
        f"{_SYSTEM}\n\n"
        f"Tone: {tone}\n"
        f"Style: {style}\n\n"
        f"<brand_brief>\n{safe_brief}\n</brand_brief>\n\n"
        f"Write {preset.batch_size} slogans."
    )