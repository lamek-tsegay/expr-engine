from __future__ import annotations

from .types import Expr, is_composite, is_number
from .evaluate import _calc


def _structurally_equal(a: Expr, b: Expr) -> bool:
    return a == b


def simplify(e: Expr) -> Expr:
    """Simplify an expression by constant-folding and basic algebraic rules.

    This is intentionally lightweight (not a full CAS), but it handles the common
    cases that make derivatives readable.
    """
    if not is_composite(e):
        return e

    op, l, r = e
    ll = simplify(l)
    rr = simplify(r)

    # Constant folding
    if is_number(ll) and is_number(rr):
        return _calc(op, ll, rr)

    # Algebraic identities
    if op == "+":
        if is_number(ll) and ll == 0:
            return rr
        if is_number(rr) and rr == 0:
            return ll
        # x + x -> 2*x (helps a lot after differentiation)
        if _structurally_equal(ll, rr):
            return ("*", 2, ll)
        # (a*x) + (b*x) -> (a+b)*x
        if is_composite(ll) and is_composite(rr) and ll[0] == "*" and rr[0] == "*":
            a1, x1 = ll[1], ll[2]
            a2, x2 = rr[1], rr[2]
            if is_number(a1) and is_number(a2) and _structurally_equal(x1, x2):
                return simplify(("*", a1 + a2, x1))
            # commuted form: (x*a) + (x*b)
            a1b, x1b = ll[2], ll[1]
            a2b, x2b = rr[2], rr[1]
            if is_number(a1b) and is_number(a2b) and _structurally_equal(x1b, x2b):
                return simplify(("*", a1b + a2b, x1b))

    if op == "-":
        if is_number(rr) and rr == 0:
            return ll
        if is_number(ll) and ll == 0:
            # 0 - x  ->  (-1) * x
            return ("*", -1, rr)
        if _structurally_equal(ll, rr):
            return 0

    if op == "*":
        if (is_number(ll) and ll == 0) or (is_number(rr) and rr == 0):
            return 0
        if is_number(ll) and ll == 1:
            return rr
        if is_number(rr) and rr == 1:
            return ll
        if is_number(ll) and ll == -1:
            return ("*", -1, rr)
        if is_number(rr) and rr == -1:
            return ("*", -1, ll)
        # (-1)*(-1*x) -> x
        if is_number(ll) and ll == -1 and is_composite(rr) and rr[0] == "*" and rr[1] == -1:
            return rr[2]

    if op == "/":
        if is_number(ll) and ll == 0:
            return 0
        if is_number(rr) and rr == 1:
            return ll
        if _structurally_equal(ll, rr):
            return 1

    return (op, ll, rr)
