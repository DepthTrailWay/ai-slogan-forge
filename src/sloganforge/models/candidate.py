"""Candidate and result schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class SloganCandidate(BaseModel):
    text: str
    score: float = Field(default=0.0, ge=0.0, le=100.0)
    tags: list[str] = Field(default_factory=list)


class ForgeResult(BaseModel):
    brief: str
    candidates: list[SloganCandidate] = Field(default_factory=list)

    def top(self, n: int = 3) -> list[SloganCandidate]:
        return self.candidates[:n]