# Contributing to ai-slogan-forge

Thanks for wanting to forge some slogans. This repo is a Windows-first
desktop tool that turns a brand brief into ranked slogan candidates using
either a hosted LLM or a local GGUF model.

## Dev setup

```powershell
git clone https://github.com/ai-slogan-forge/ai-slogan-forge.git
cd ai-slogan-forge
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e ".[dev]"
```

Optional local inference backend:

```powershell
pip install -e ".[local]"
```

## Running

```powershell
slogan-forge --brief "eco-friendly cold brew, urban commuters, bold"
```

or launch the Tkinter shell:

```powershell
python -m sloganforge.bootstrap.launcher --gui
```

## Layout

- `src/sloganforge/bootstrap/` — entry points, CLI + GUI launchers
- `src/sloganforge/core/` — generation engine, prompt construction, ranking
- `src/sloganforge/handlers/` — feature handlers (batch, export, refine)
- `src/sloganforge/services/` — LLM backends, cache, telemetry-off
- `src/sloganforge/models/` — pydantic schemas for briefs, candidates
- `src/sloganforge/utils/` — text hygiene, dedupe, scoring helpers
- `src/sloganforge/config/` — settings loader, presets

## Style

- `ruff check src tests` must pass.
- `mypy src` must pass.
- New handlers get a matching test under `tests/`.

## Commit style

Conventional commits: `feat(core): add cadence scorer`, `fix(services): retry on 429`.

## Pull requests

Keep PRs scoped to one handler or one service. Include a sample brief and
the top-3 output in the PR description so reviewers can eyeball quality.