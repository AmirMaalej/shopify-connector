"""
Tag utilities: priority parsing and whitelist/blacklist handling.
"""

from __future__ import annotations

from typing import Iterable, List, Optional


def parse_order_priority(tags: Iterable[str]) -> Optional[int]:
    """TODO: derive priority 1-100 from messy tags."""
    raise NotImplementedError


def is_excluded(tags: Iterable[str], whitelist: List[str], blacklist: List[str]) -> bool:
    """TODO: apply whitelist/blacklist semantics."""
    raise NotImplementedError
