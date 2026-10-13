"""Tiny on-disk cache keyed by prompt hash.

Avoids re-billing the same brief twice. TTL is 24h by default.
"""

from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path


class PromptCache:
    def __init__(self, root: Path, ttl_s: int = 86_400) -> None:
        self._root = root
        self._root.mkdir(parents=True, exist_ok=True)
        self._ttl = ttl_s

    def _key(self, prompt: str) -> Path:
        digest = hashlib.sha256(prompt.encode("utf-8")).hexdigest()[:24]
        return self._root / f"{digest}.json"

    def get(self, prompt: str) -> list[str] | None:
        path = self._key(prompt)
        if not path.exists():
            return None
        blob = json.loads(path.read_text(encoding="utf-8"))
        if time.time() - blob["ts"] > self._ttl:
            path.unlink(missing_ok=True)
            return None
        return blob["lines"]

    def put(self, prompt: str, lines: list[str]) -> None:
        self._key(prompt).write_text(
            json.dumps({"ts": time.time(), "lines": lines}), encoding="utf-8"
        )