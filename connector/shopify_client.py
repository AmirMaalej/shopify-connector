"""
Shopify GraphQL client with pagination and throttling/backoff.
"""

from __future__ import annotations

import math
import time
from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional

import httpx

from . import shopify_queries


class ShopifyClient:
    """Thin wrapper around httpx for Shopify GraphQL."""

    def __init__(self, store: str, token: str) -> None:
        self.store = store
        self.token = token
        self._client = httpx.Client(timeout=30.0)

    def _store_domain(self) -> str:
        """
        Return full myshopify domain from subdomain or passthrough if already a host.
        """
        if self.store.startswith("http://") or self.store.startswith("https://"):
            trimmed = self.store.split("://", 1)[1]
        else:
            trimmed = self.store
        if "." in trimmed:
            return trimmed
        return f"{trimmed}.myshopify.com"

    def _log_cost(self, cost_info: Dict[str, Any]) -> None:
        """
        Log query cost and throttle status in one concise line.
        """
        if not cost_info:
            return
        requested = cost_info.get("requestedQueryCost")
        actual = cost_info.get("actualQueryCost")
        throttle = cost_info.get("throttleStatus") or {}
        available = throttle.get("currentlyAvailable")
        rate = throttle.get("restoreRate")
        parts = [
            f"requested={requested}" if requested is not None else None,
            f"actual={actual}" if actual is not None else None,
            f"available={available}" if available is not None else None,
            f"restoreRate={rate}" if rate is not None else None,
        ]
        print("Shopify cost: " + ", ".join(p for p in parts if p is not None))

    def _backoff_if_needed(self, throttle_status: Dict[str, Any], requested_cost: int) -> None:
        """
        Sleep if currentlyAvailable is below requested cost.
        Sleep seconds = max(1, ceil((requested - available)/restoreRate)), capped at 20s.
        """
        if not throttle_status:
            return
        available = throttle_status.get("currentlyAvailable")
        rate = throttle_status.get("restoreRate") or 1
        if available is None:
            return
        if requested_cost is None:
            requested_cost = 1
        if available >= requested_cost:
            return
        deficit = max(0, requested_cost - available)
        wait_seconds = math.ceil(deficit / rate)
        wait_seconds = max(1, min(wait_seconds, 20))
        time.sleep(wait_seconds)

    def _run_query(self, query: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute GraphQL query with retry/backoff on throttling.
        """
        url = f"https://{self._store_domain()}/admin/api/2024-01/graphql.json"
        headers = {"X-Shopify-Access-Token": self.token}
        max_retries = 5
        backoff = 1

        for attempt in range(max_retries):
            resp = self._client.post(url, json={"query": query, "variables": variables}, headers=headers)
            if resp.status_code != 200:
                snippet = resp.text[:200]
                raise RuntimeError(f"Shopify API error {resp.status_code}: {snippet}")

            payload = resp.json()
            cost_info = (payload.get("extensions") or {}).get("cost") or {}
            throttle_status = cost_info.get("throttleStatus") or {}
            self._log_cost(cost_info)
            requested_cost = cost_info.get("requestedQueryCost") or 1
            self._backoff_if_needed(throttle_status, requested_cost)

            errors = payload.get("errors") or []
            if errors:
                messages = " ".join(e.get("message", "") for e in errors).lower()
                if "throttl" in messages and attempt < max_retries - 1:
                    sleep_for = min(20, backoff)
                    time.sleep(sleep_for)
                    backoff *= 2
                    continue
                raise RuntimeError(f"Shopify GraphQL errors: {errors}")

            data = payload.get("data")
            if data is not None:
                return data

            if attempt < max_retries - 1:
                sleep_for = min(20, backoff)
                time.sleep(sleep_for)
                backoff *= 2

        raise RuntimeError("Shopify GraphQL request failed after retries")

    def fetch_recent_orders(self, days: int = 14) -> List[Dict[str, Any]]:
        """
        Fetch orders from the last `days` days using cursor-based pagination.
        """
        cutoff = datetime.utcnow() - timedelta(days=days)
        cutoff_iso = cutoff.replace(microsecond=0).isoformat() + "Z"
        query_filter = f"created_at:>={cutoff_iso}"
        first = 50
        after: Optional[str] = None
        orders: List[Dict[str, Any]] = []

        while True:
            variables = {"first": first, "after": after, "query": query_filter}
            data = self._run_query(shopify_queries.ORDERS_QUERY, variables)
            orders_conn = (data or {}).get("orders") or {}
            nodes = orders_conn.get("nodes") or []
            orders.extend(nodes)
            page_info = orders_conn.get("pageInfo") or {}
            has_next = page_info.get("hasNextPage")
            after = page_info.get("endCursor")
            if not has_next or not after:
                break

        return orders

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> "ShopifyClient":
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        self.close()
