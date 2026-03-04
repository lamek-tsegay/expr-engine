from __future__ import annotations

from .types import Expr, is_composite, is_number, is_variable

_PRECEDENCE = {
    "+": 1,
    "-": 1,
    "*": 2,
    "/": 2,
}

def _needs_parens(parent_op: str, child: Expr, is_right: bool) -> bool:
    if not is_composite(child):
        return False
    child_op = child[0]
    if _PRECEDENCE[child_op] < _PRECEDENCE[parent_op]:
        return True
    # Handle non-associative cases to preserve meaning:
    # a - (b - c), a / (b / c), a / (b * c), etc.
    if is_right and parent_op in ("-", "/") and _PRECEDENCE[child_op] == _PRECEDENCE[parent_op]:
        return True
    return False


def pretty(e: Expr) -> str:
    """Return a human-readable string for an expression."""
    if is_number(e):
        # Print ints cleanly
        if isinstance(e, bool):
            return str(int(e))
        if isinstance(e, float) and e.is_integer():
            return str(int(e))
        return str(e)

    if is_variable(e):
        return e

    if not is_composite(e):
        return str(e)

    op, l, r = e
    ls = pretty(l)
    rs = pretty(r)

    if _needs_parens(op, l, is_right=False):
        ls = f"({ls})"
    if _needs_parens(op, r, is_right=True):
        rs = f"({rs})"

    return f"{ls}{op}{rs}"
