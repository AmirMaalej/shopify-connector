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

## Design notes & trade-offs

- Implemented as a dry-run connector only; request is prepared but not sent, as requested.
- Used best-effort mapping to the everstox payload schema with explicit placeholders for missing data.
- Filtering is defensive: orders with no remaining quantities are excluded even if Shopify status is inconsistent.
- Chose synchronous HTTP for simplicity and readability under time constraints.
- With more time, I would add:
- unit tests for tag parsing and filtering
- better schema validation for payload
- configurable date range and page size

## Setup

- Python 3.10+
- Install deps: `pip install -r requirements.txt`
- Optionally load env vars from `.env` (see `connector/config.py` for keys).

## Usage

Run CLI (dry-run default enabled via env):
```
python cli.py --dry-run
```

## Design notes & trade-offs

- Implemented as a dry-run connector only; request is prepared but not sent, as requested.
- Used best-effort mapping to the everstox payload schema with explicit placeholders for missing data.
- Filtering is defensive: orders with no remaining quantities are excluded even if Shopify status is inconsistent.
- Chose synchronous HTTP for simplicity and readability under time constraints.
- With more time, I would add:
  - unit tests for tag parsing and filtering
  - better schema validation for payload
  - configurable date range and page size
