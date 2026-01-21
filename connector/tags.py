"""
Tag utilities: priority parsing and whitelist/blacklist handling.
"""

from __future__ import annotations

import re
from typing import Iterable, List, Optional


def parse_order_priority(tags: Iterable[str]) -> Optional[int]:
    """
    Derive priority 1-100 from messy tags; returns max if multiple matches.
    """
    priorities: List[int] = []
    normalized = [t.strip().lower() for t in tags if t is not None]

    for tag in normalized:
        if "urgent" in tag:
            priorities.append(90)
        if "vip" in tag:
            priorities.append(80)
        for match in re.findall(r"(?:priority|prio|\bp)\s*[:=]?\s*(\d{1,3})", tag):
            try:
                priorities.append(int(match))
            except ValueError:
                continue

    if not priorities:
        return None

    priority = max(priorities)
    return max(1, min(priority, 100))


def is_excluded(tags: Iterable[str], whitelist: List[str], blacklist: List[str]) -> bool:
    """
    Apply blacklist/whitelist semantics; blacklist wins, whitelist requires a match when provided.
    """
    normalized_tags = [t.strip().lower() for t in tags if t is not None]
    normalized_whitelist = [w.strip().lower() for w in whitelist if w]
    normalized_blacklist = [b.strip().lower() for b in blacklist if b]

    def matches(rule: str) -> bool:
        return any(rule in tag for tag in normalized_tags)

    for rule in normalized_blacklist:
        if matches(rule):
            return True

    if normalized_whitelist:
        if not any(matches(rule) for rule in normalized_whitelist):
            return True

    return False
