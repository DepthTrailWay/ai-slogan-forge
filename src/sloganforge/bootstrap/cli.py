"""Argument parser shared by launcher and tests."""

from __future__ import annotations

import argparse


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="slogan-forge",
        description="Generate ranked slogan / tagline candidates from a brand brief.",
    )
    parser.add_argument(
        "--brief",
        "-b",
        required=False,
        default="",
        help="Brand brief: product, audience, tone. Free text.",
    )
    parser.add_argument(
        "--count",
        "-n",
        type=int,
        default=10,
        help="Number of candidates to keep after ranking (default: 10).",
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the Tkinter desktop shell instead of the CLI.",
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose logging.",
    )
    return parser