"""Minimal Tkinter shell for the slogan forge.

Kept deliberately thin: the shell collects a brief and a count, calls the
same engine the CLI uses, and renders the ranked list. No business logic
lives here.
"""

from __future__ import annotations

import asyncio
import tkinter as tk
from tkinter import ttk

from sloganforge.config.settings import load_settings
from sloganforge.core.engine import SloganEngine
from sloganforge.services.factory import build_backend


def launch() -> None:
    settings = load_settings()
    engine = SloganEngine(backend=build_backend(settings), settings=settings)

    root = tk.Tk()
    root.title("ai-slogan-forge")
    root.geometry("720x520")

    ttk.Label(root, text="Brand brief").pack(anchor="w", padx=12, pady=(12, 2))
    brief_box = tk.Text(root, height=5, wrap="word")
    brief_box.pack(fill="x", padx=12)

    out = tk.Text(root, height=18, wrap="word", state="disabled")
    out.pack(fill="both", expand=True, padx=12, pady=12)

    def on_forge() -> None:
        brief = brief_box.get("1.0", "end").strip()
        result = asyncio.run(engine.forge(brief=brief, count=10))
        out.configure(state="normal")
        out.delete("1.0", "end")
        for rank, c in enumerate(result.candidates, start=1):
            out.insert("end", f"{rank:>2}. [{c.score:5.1f}] {c.text}\n")
        out.configure(state="disabled")

    ttk.Button(root, text="Forge", command=on_forge).pack(pady=(0, 12))
    root.mainloop()