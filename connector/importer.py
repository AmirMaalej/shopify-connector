"""
Import orchestration: fetch, filter, transform, summarize.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple

from .config import Settings
from .shopify_client import ShopifyClient
from .tags import is_excluded, parse_order_priority
from .transform import to_everstox_payload


def import_orders(settings: Settings) -> Dict[str, Any]:
    """TODO: orchestrate import flow and produce summary."""
    raise NotImplementedError


def _filter_orders(
    orders: Iterable[Dict[str, Any]],
    whitelist: List[str],
    blacklist: List[str],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """TODO: filter orders and return included/excluded lists."""
    raise NotImplementedError


def _summarize(excluded: List[Dict[str, Any]], sent: List[Dict[str, Any]]) -> Dict[str, Any]:
    """TODO: summarize import results and exclusions."""
    raise NotImplementedError
