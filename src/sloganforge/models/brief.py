"""Structured brief schema.

A brief can come in as free text (the common case) or as a structured
form from the GUI. The engine only needs the rendered text.
"""

from __future__ import annotations

from pydantic import BaseModel, Field


class BrandBrief(BaseModel):
    product: str = ""
    audience: str = ""
    tone: str = "confident"
    keywords: list[str] = Field(default_factory=list)

    def render(self) -> str:
        parts = [self.product, self.audience, f"tone: {self.tone}"]
        if self.keywords:
            parts.append("keywords: " + ", ".join(self.keywords))
        return " | ".join(p for p in parts if p)