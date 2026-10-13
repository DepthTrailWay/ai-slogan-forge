"""Process entry point for ai-slogan-forge.

Dispatches to the CLI or the Tkinter shell depending on argv. Owns the
top-level exception boundary so a bad brief never dumps a raw traceback
into the user's console.
"""

from __future__ import annotations

import argparse
import asyncio
import logging
import sys

from sloganforge.bootstrap.cli import build_parser
from sloganforge.config.settings import load_settings
from sloganforge.core.engine import SloganEngine
from sloganforge.services.factory import build_backend
from sloganforge.utils.logging_setup import configure_logging

log = logging.getLogger("sloganforge.launcher")


def _run_cli(args: argparse.Namespace) -> int:
    settings = load_settings()
    backend = build_backend(settings)
    engine = SloganEngine(backend=backend, settings=settings)
    result = asyncio.run(engine.forge(brief=args.brief, count=args.count))
    for rank, candidate in enumerate(result.candidates, start=1):
        print(f"{rank:>2}. [{candidate.score:5.1f}] {candidate.text}")
    return 0


def _run_gui() -> int:
    from sloganforge.bootstrap.gui_shell import launch

    launch()
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    configure_logging(verbose=args.verbose)
    try:
        if args.gui:
            return _run_gui()
        return _run_cli(args)
    except KeyboardInterrupt:
        log.info("interrupted by user")
        return 130
    except Exception as exc:  # top-level boundary
        log.error("forge failed: %s", exc, exc_info=args.verbose)
        return 1


if __name__ == "__main__":
    sys.exit(main())