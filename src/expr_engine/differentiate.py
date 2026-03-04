from __future__ import annotations

from .types import Expr, is_composite, is_number, is_variable


def differentiate(e: Expr, x: str) -> Expr:
    """Symbolically differentiate expression e with respect to variable x."""
    # Leaves
    if is_variable(e):
        return 1 if e == x else 0
    if is_number(e):
        return 0

    # Composite
    if not is_composite(e):
        raise TypeError(f"Unsupported expression node: {type(e).__name__}")

    op, left, right = e

    if op == "+":
        return ("+", differentiate(left, x), differentiate(right, x))

    if op == "-":
        return ("-", differentiate(left, x), differentiate(right, x))

    if op == "*":
        # product rule: (u*v)' = u'*v + u*v'
        return (
            "+",
            ("*", differentiate(left, x), right),
            ("*", left, differentiate(right, x)),
        )

    if op == "/":
        # quotient rule: (u/v)' = (u'*v - u*v') / (v*v)
        return (
            "/",
            (
                "-",
                ("*", differentiate(left, x), right),
                ("*", left, differentiate(right, x)),
            ),
            ("*", right, right),
        )

    raise ValueError(f"Unsupported operator for differentiation: {op}")
