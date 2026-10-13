"""Backend factory. Picks hosted vs local from settings."""

from __future__ import annotations

from sloganforge.config.settings import Settings
from sloganforge.services.backend import SloganBackend


def build_backend(settings: Settings) -> SloganBackend:
    if settings.backend == "local":
        from sloganforge.services.local_backend import LocalBackend

        return LocalBackend(settings)
    from sloganforge.services.hosted_backend import HostedBackend

    return HostedBackend(settings)