# everstox Shopify connector

Minimal scaffold for the Shopify→everstox import challenge. Business logic is intentionally TODO.

## Setup

- Python 3.10+
- Install deps: `pip install -r requirements.txt`
- Optionally load env vars from `.env` (see `connector/config.py` for keys).

## Usage

Run CLI (dry-run default enabled via env):
```
python cli.py --dry-run
```

## Notes

Implementation steps pending: Shopify GraphQL fetch, throttling/backoff, tag parsing, whitelist/blacklist, transform to everstox payload, request preparation, and summary output.
