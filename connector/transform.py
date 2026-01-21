"""
Transform Shopify orders into everstox payloads.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List


def transform_order(order: Dict[str, Any]) -> Dict[str, Any]:
    """TODO: map single Shopify order to everstox order shape."""
    raise NotImplementedError


def to_everstox_payload(orders: Iterable[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """TODO: bundle transformed orders into final payload."""
    raise NotImplementedError
