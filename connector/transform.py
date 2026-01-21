"""
Transform Shopify orders into everstox payloads.

Best-effort mapping to the target schema described in the challenge.
Unknown / unavailable fields are filled with explicit placeholders.
"""

from __future__ import annotations

from typing import Any, Dict, Iterable, List, Optional


def to_everstox_payload(orders: Iterable[Dict[str, Any]], shop_instance_id: str) -> List[Dict[str, Any]]:
    return [transform_order(order, shop_instance_id=shop_instance_id) for order in orders]


def transform_order(order: Dict[str, Any], shop_instance_id: str) -> Dict[str, Any]:
    """
    Map a Shopify order dict to a best-effort everstox order shape.
    """

    shipping_money = _shop_money(order.get("totalShippingPriceSet"))
    tax_money = _shop_money(order.get("totalTaxSet"))
    total_money = _shop_money(order.get("totalPriceSet"))

    priority = order.get("order_priority")
    if isinstance(priority, int):
        # Spec is slightly inconsistent (mentions 1-100 and 1-99). We clamp to 1-99 for payload safety.
        priority = max(1, min(priority, 99))
    else:
        priority = None

    shipping_address = _map_address(order.get("shippingAddress"))
    billing_address = _map_address(order.get("billingAddress"))

    items: List[Dict[str, Any]] = []
    for item in order.get("remaining_line_items", []):
        sku = item.get("sku") or (item.get("variant") or {}).get("sku") or "UNKNOWN_SKU"
        qty = item.get("remaining_qty")
        if not isinstance(qty, int) or qty <= 0:
            continue
        items.append(
            {
                "quantity": qty,
                "product": {"sku": sku},
            }
        )

    # Minimal shipping_price structure: currency + gross price, and explicit placeholders for unknown fields
    shipping_price = None
    if shipping_money:
        shipping_price = {
            "currency": shipping_money.get("currency"),
            "price": _to_float(shipping_money.get("amount")),
            "tax": 0.0,
            "net": 0.0,
        }

    # Totals (optional, but useful in payload if schema accepts it)
    totals = None
    if total_money:
        totals = {
            "currency": total_money.get("currency"),
            "total": _to_float(total_money.get("amount")),
            "tax": _to_float(tax_money.get("amount")) if tax_money else 0.0,
        }

    return {
        "shop_instance_id": shop_instance_id,
        "order_number": order.get("name"),
        "order_date": order.get("createdAt"),
        "financial_status": order.get("displayFinancialStatus"),
        "order_priority": priority,
        "customer_email": _customer_email(order),
        "shipping_address": shipping_address,
        "billing_address": billing_address,
        "shipping_price": shipping_price,
        "totals": totals,
        "order_items": items,
    }


def _customer_email(order: Dict[str, Any]) -> str:
    customer = order.get("customer") or {}
    email = customer.get("email")
    return email or "UNKNOWN_EMAIL"


def _map_address(addr: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not addr:
        return None
    # Shopify address fields vary; we map common ones with safe fallbacks
    return {
        "first_name": addr.get("firstName") or "",
        "last_name": addr.get("lastName") or "",
        "company": addr.get("company") or "",
        "address_1": addr.get("address1") or "",
        "address_2": addr.get("address2") or "",
        "city": addr.get("city") or "",
        "zip": addr.get("zip") or "",
        "country_code": addr.get("countryCodeV2") or addr.get("countryCode") or "",
        "phone": addr.get("phone") or "",
    }


def _shop_money(money_set: Optional[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
    if not money_set:
        return None
    shop_money = money_set.get("shopMoney") or {}
    amount = shop_money.get("amount")
    currency = shop_money.get("currencyCode")
    if amount is None and currency is None:
        return None
    return {"amount": amount, "currency": currency}


def _to_float(value: Any) -> float:
    try:
        return float(value)
    except Exception:
        return 0.0
