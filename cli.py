"""
CLI entry point for the everstox Shopify connector.
"""

from __future__ import annotations

import argparse
import sys

from connector.config import load_settings
from connector.importer import import_orders


def main(argv: list[str] | None = None) -> int:
    """Parse arguments and run import."""
    parser = argparse.ArgumentParser(description="everstox Shopify connector")
    parser.add_argument("--dry-run", action="store_true", help="Run without sending requests")
    args = parser.parse_args(argv)

    settings = load_settings()
    if args.dry_run:
        settings.dry_run = True

    # TODO: invoke import and print summary.
    import_orders(settings)
    return 0


if __name__ == "__main__":
    sys.exit(main())
