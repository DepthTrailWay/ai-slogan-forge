"""Export handler: write forge results to disk.

Supports plain text, markdown, and JSON. Never overwrites silently — the
caller must pass `overwrite=True` for that.
"""

from __future__ import annotations

import json
from pathlib import Path

from sloganforge.models.candidate import ForgeResult


def export_text(result: ForgeResult, path: Path, overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass overwrite=True")
    lines = [f"{i}. [{c.score:5.1f}] {c.text}" for i, c in enumerate(result.candidates, 1)]
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return path


def export_json(result: ForgeResult, path: Path, overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass overwrite=True")
    path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    return path


def export_markdown(result: ForgeResult, path: Path, overwrite: bool = False) -> Path:
    if path.exists() and not overwrite:
        raise FileExistsError(f"{path} exists; pass overwrite=True")
    body = [f"# Slogans for: {result.brief}", ""]
    for i, c in enumerate(result.candidates, 1):
        body.append(f"{i}. **{c.text}**  \n   _score {c.score:.1f}_")
    path.write_text("\n".join(body) + "\n", encoding="utf-8")
    return path