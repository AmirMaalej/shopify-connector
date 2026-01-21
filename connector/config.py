"""
Configuration loading for the Shopify connector.
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    load_dotenv = None


@dataclass
class Settings:
    """Placeholder settings container."""

    shopify_store: Optional[str] = None
    shopify_token: Optional[str] = None
    everstox_shop_id: Optional[str] = None
    tag_whitelist: Optional[str] = None
    tag_blacklist: Optional[str] = None
    dry_run: bool = True


def load_settings() -> Settings:
    """
    Load settings from environment (and .env if available).
    TODO: implement parsing and validation.
    """
    if load_dotenv:
        load_dotenv()
    return Settings(
        shopify_store=os.getenv("SHOPIFY_STORE"),
        shopify_token=os.getenv("SHOPIFY_TOKEN"),
        everstox_shop_id=os.getenv("EVERSTOX_SHOP_ID"),
        tag_whitelist=os.getenv("TAG_WHITELIST"),
        tag_blacklist=os.getenv("TAG_BLACKLIST"),
        dry_run=os.getenv("DRY_RUN", "true").lower() == "true",
    )
