from __future__ import annotations

from typing import Mapping
from .types import Expr, IllegalOperator, is_composite, is_number, is_variable


def _calc(op: str, left, right):
    if op == "+":
        return left + right
    if op == "-":
        return left - right
    if op == "*":
        return left * right
    if op == "/":
        return left / right
    raise IllegalOperator(op)


def evaluate(e: Expr, env: Mapping[str, float] | None = None):
    """Evaluate an expression given an environment mapping variables to values."""
    env = {} if env is None else dict(env)

    if is_composite(e):
        op, l, r = e
        return _calc(op, evaluate(l, env), evaluate(r, env))

    if is_variable(e):
        if e not in env:
            raise KeyError(f"Missing value for variable '{e}'")
        return env[e]

    if is_number(e):
        return e

    # Defensive: shouldn't happen if Expr typing is respected.
    raise TypeError(f"Unsupported expression leaf: {type(e).__name__}")
