from __future__ import annotations

from typing import Set
from .types import Expr, is_composite, is_variable


def variables(e: Expr) -> Set[str]:
    """Return the set of variable names used by an expression."""
    if is_composite(e):
        _, l, r = e
        return variables(l) | variables(r)
    if is_variable(e):
        return {e}
    return set()
