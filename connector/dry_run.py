"""
Dry-run helpers for preparing everstox requests without sending them.
"""

from __future__ import annotations

from typing import Any, Dict, List


def build_request(shop_id: str, payload: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Construct POST request details to everstox endpoint without sending.
    """
    url = f"https://api.demo.everstox.com/shops/{shop_id}/orders"
    return {
        "method": "POST",
        "url": url,
        "headers": {
            "Content-Type": "application/json",
        },
        "json": payload,
    }
