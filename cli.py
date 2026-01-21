"""
CLI entry point for the everstox Shopify connector.
"""

from __future__ import annotations

import argparse
import sys

from connector.config import load_settings
from connector.importer import import_orders
from pprint import pprint


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and run import."""
    parser = argparse.ArgumentParser(description="everstox Shopify connector")
    parser.add_argument("--dry-run", action="store_true", help="Run without sending requests")
    args = parser.parse_args(argv)

    settings = load_settings()
    if args.dry_run:
        settings.dry_run = True

    result = import_orders(settings)

    print("Summary:")
    pprint(result.get("summary"))

    excluded_sample = result.get("excluded_sample") or []
    if excluded_sample:
        print("Excluded sample (up to 5):")
        pprint(excluded_sample)

    prepared = result.get("prepared_request") or {}
    payload = prepared.get("json") or []
    print("Prepared request:")
    print(f"{prepared.get('method')} {prepared.get('url')}")
    print(f"Payload orders: {len(payload)}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
