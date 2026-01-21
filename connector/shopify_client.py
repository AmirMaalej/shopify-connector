"""
Shopify GraphQL client scaffolding with pagination and throttling hooks.
"""

from __future__ import annotations

import httpx
from typing import Any, Dict, Iterable

from . import shopify_queries


class ShopifyClient:
    """Thin wrapper around httpx for Shopify GraphQL. TODO: implement methods."""

    def __init__(self, store: str, token: str) -> None:
        self.store = store
        self.token = token
        self._client = httpx.Client(timeout=30.0)

    def _run_query(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """TODO: execute GraphQL query and handle errors."""
        raise NotImplementedError

    def _log_cost(self, cost_info: Dict[str, Any]) -> None:
        """TODO: log query cost and throttle status."""
        raise NotImplementedError

    def _backoff_if_needed(self, throttle_status: Dict[str, Any]) -> None:
        """TODO: implement backoff based on throttle status."""
        raise NotImplementedError

    def fetch_recent_orders(self) -> Iterable[Dict[str, Any]]:
        """TODO: paginate orders for the last 14 days."""
        raise NotImplementedError

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> "ShopifyClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
