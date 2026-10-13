"""Backend protocol.

A backend takes a prompt and returns a list of raw candidate strings. That
is the whole contract. Hosted, local, and mock backends all satisfy it.
"""

from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class SloganBackend(Protocol):
    async def generate(self, prompt: str, n: int) -> list[str]:
        """Return up to `n` raw slogan strings for `prompt`."""
        ...

    async def aclose(self) -> None:
        """Release any held resources (sockets, model handles)."""
        ...