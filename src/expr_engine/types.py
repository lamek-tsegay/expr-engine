from __future__ import annotations

from dataclasses import dataclass
from numbers import Number
from typing import Dict, Tuple, Union, Any

# Expression representation:
# - Number (int/float)
# - variable name (str)
# - composite tuple: (op, left, right) where op in {"+","-","*","/"}
Expr = Union[Number, str, Tuple[str, "Expr", "Expr"]]


class IllegalOperator(Exception):
    """Raised when an unknown operator is encountered."""
    pass


class ParseError(ValueError):
    """Raised when parsing fails."""
    pass


def is_number(e: Expr) -> bool:
    return isinstance(e, Number)


def is_variable(e: Expr) -> bool:
    return isinstance(e, str)


def is_composite(e: Expr) -> bool:
    return isinstance(e, tuple) and len(e) == 3 and isinstance(e[0], str)
