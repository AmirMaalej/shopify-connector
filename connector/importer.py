"""
Import orchestration: fetch, filter, transform, summarize.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Tuple

from .config import Settings
from .dry_run import build_request
from .shopify_client import ShopifyClient
from .tags import is_excluded, parse_order_priority
from .transform import to_everstox_payload


def import_orders(settings: Settings) -> Dict[str, Any]:
    """
    Orchestrate import flow (dry-run): fetch -> filter -> transform -> build request.
    """
    whitelist = [w.strip() for w in (settings.tag_whitelist or "").split(",") if w.strip()]
    blacklist = [b.strip() for b in (settings.tag_blacklist or "").split(",") if b.strip()]

    with ShopifyClient(settings.shopify_store, settings.shopify_token) as client:
        fetched_orders = client.fetch_recent_orders(14)

    included, excluded = _filter_orders(fetched_orders, whitelist, blacklist)

    shop_instance_id = settings.everstox_shop_id or "SHOP_INSTANCE_UUID"
    payload = to_everstox_payload(included, shop_instance_id=shop_instance_id)
    prepared_request = build_request(shop_instance_id, payload)

    prepared_request = build_request(settings.everstox_shop_id or "", payload)

    summary = _summarize(excluded, included)
    excluded_sample = [
        {"id": o.get("id"), "name": o.get("name"), "reason": o.get("exclude_reason")}
        for o in excluded[:5]
    ]

    return {
        "summary": summary,
        "prepared_request": prepared_request,
        "excluded_sample": excluded_sample,
    }


def _filter_orders(
    orders: Iterable[Dict[str, Any]],
    whitelist: List[str],
    blacklist: List[str],
) -> Tuple[List[Dict[str, Any]], List[Dict[str, Any]]]:
    """
    Filter orders and attach derived fields; return (included, excluded).

    Rules:
    - Exclude if not paid
    - Exclude if fully fulfilled
    - Exclude if excluded by tag rules
    - Exclude if no remaining quantities on any line item (defensive)
    """
    included: List[Dict[str, Any]] = []
    excluded: List[Dict[str, Any]] = []

    for order in orders:
        tags = order.get("tags") or []
        reason: str | None = None

        if order.get("displayFinancialStatus") != "PAID":
            reason = "not_paid"
        elif order.get("displayFulfillmentStatus") == "FULFILLED":
            reason = "fulfilled"
        elif is_excluded(tags, whitelist, blacklist):
            reason = "tag_excluded"

        priority = parse_order_priority(tags)

        # Compute remaining quantities (include partial fulfillment)
        remaining_items: List[Dict[str, Any]] = []
        line_items = (order.get("lineItems") or {}).get("nodes", [])
        for item in line_items:
            qty = item.get("quantity") or 0
            fulfilled = item.get("fulfilledQuantity") or 0
            remaining_qty = qty - fulfilled
            if remaining_qty > 0:
                item_with_remaining = dict(item)
                item_with_remaining["remaining_qty"] = remaining_qty
                remaining_items.append(item_with_remaining)

        # Defensive exclusion: avoids building payloads with empty line items
        if reason is None and not remaining_items:
            reason = "no_remaining_items"

        if reason:
            marked = dict(order)
            marked["exclude_reason"] = reason
            marked["order_priority"] = priority
            excluded.append(marked)
            continue

        enriched = dict(order)
        enriched["order_priority"] = priority
        enriched["remaining_line_items"] = remaining_items
        included.append(enriched)

    return included, excluded


def _summarize(excluded: List[Dict[str, Any]], included: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Summarize import results with simple counts and exclusion reasons.
    """
    summary: Dict[str, Any] = {}
    summary["fetched_total"] = len(excluded) + len(included)
    summary["eligible_total"] = len(included)
    summary["excluded_total"] = len(excluded)

    reason_counts: Dict[str, int] = {}
    for order in excluded:
        reason = order.get("exclude_reason") or "unknown"
        reason_counts[reason] = reason_counts.get(reason, 0) + 1
    if reason_counts:
        summary["exclusion_reasons"] = reason_counts

    return summary
