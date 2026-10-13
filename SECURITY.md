# Security Policy

## Supported versions

| Version | Supported |
| ------- | --------- |
| 0.7.x   | yes       |
| 0.6.x   | security fixes only |
| < 0.6   | no        |

## Reporting a vulnerability

Email `security@ai-slogan-forge.dev` with a description, a repro, and the
affected version. Do not open a public issue for anything that could leak
API keys, prompt-injection vectors, or local model paths.

We aim to acknowledge within 72 hours and ship a patch within 14 days for
confirmed issues.

## Threat model

ai-slogan-forge talks to two things: a hosted LLM endpoint (configurable)
and the local filesystem. The interesting attack surfaces are:

- **Prompt injection via brand brief.** Briefs are user-supplied. The
  engine wraps the brief in a delimited block and strips control tokens
  before it hits the model. See `utils/sanitize.py`.
- **API key leakage.** Keys live in `.env` or the OS keyring. They are
  never written to logs. The logger redacts anything matching the key
  fingerprint.
- **Local model path traversal.** `services/local_backend.py` validates
  that the GGUF path resolves inside the configured `models/` root.

## Out of scope

Slogan quality, brand taste, and whether "Just Do It" was already taken.