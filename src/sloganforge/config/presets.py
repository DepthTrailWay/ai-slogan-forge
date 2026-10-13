"""Tone/style presets.

A preset shapes the prompt and biases the scorer. Add new ones here; the
loader picks them up by name from SF_PRESET.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class Preset:
    name: str
    tone: str
    style: str
    batch_size: int
    score_bias: float


DEFAULT_PRESET = Preset(
    name="balanced",
    tone="confident, human, warm",
    style="short declarative lines, occasional rhyme",
    batch_size=24,
    score_bias=0.0,
)

PRESETS: dict[str, Preset] = {
    "balanced": DEFAULT_PRESET,
    "punchy": Preset(
        name="punchy",
        tone="bold, high-energy, imperative",
        style="verb-first, 3-5 words, hard consonants",
        batch_size=24,
        score_bias=2.0,
    ),
    "premium": Preset(
        name="premium",
        tone="restrained, aspirational, understated",
        style="noun phrases, no exclamation, luxury cadence",
        batch_size=20,
        score_bias=1.5,
    ),
    "playful": Preset(
        name="playful",
        tone="witty, irreverent, friendly",
        style="wordplay, alliteration, mild absurdity",
        batch_size=28,
        score_bias=1.0,
    ),
}