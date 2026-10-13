"""Logging configuration with API-key redaction."""

from __future__ import annotations

import logging
import re

_KEY_PAT = re.compile(r"(sk-[A-Za-z0-9]{8})[A-Za-z0-9]+")


class _RedactFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:
        if isinstance(record.msg, str):
            record.msg = _KEY_PAT.sub(r"\1…REDACTED", record.msg)
        return True


def configure_logging(verbose: bool = False) -> None:
    level = logging.DEBUG if verbose else logging.INFO
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))
    handler.addFilter(_RedactFilter())
    root = logging.getLogger()
    root.handlers.clear()
    root.addHandler(handler)
    root.setLevel(level)