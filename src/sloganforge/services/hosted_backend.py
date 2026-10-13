"""Hosted LLM backend.

Talks to an OpenAI-compatible chat completions endpoint. Retries 429 and
5xx with exponential backoff via tenacity. The API key never appears in
logs — the logger redacts by fingerprint.
"""

from __future__ import annotations

import logging

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from sloganforge.config.settings import Settings

log = logging.getLogger("sloganforge.services.hosted")


class HostedBackend:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings
        self._client = httpx.AsyncClient(
            base_url=settings.endpoint,
            timeout=settings.timeout_s,
            headers={"Authorization": f"Bearer {settings.api_key}"},
        )

    @retry(
        retry=retry_if_exception_type(httpx.HTTPStatusError),
        wait=wait_exponential(multiplier=1, min=1, max=20),
        stop=stop_after_attempt(4),
        reraise=True,
    )
    async def generate(self, prompt: str, n: int) -> list[str]:
        payload = {
            "model": self._settings.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": self._settings.temperature,
            "n": 1,
        }
        resp = await self._client.post("/chat/completions", json=payload)
        if resp.status_code in (429, 500, 502, 503, 504):
            resp.raise_for_status()
        resp.raise_for_status()
        text = resp.json()["choices"][0]["message"]["content"]
        return [line for line in text.splitlines() if line.strip()]

    async def aclose(self) -> None:
        await self._client.aclose()