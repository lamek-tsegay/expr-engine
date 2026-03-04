from __future__ import annotations

import re
from dataclasses import dataclass
from typing import List, Optional

from .types import Expr, ParseError

_TOKEN_RE = re.compile(
    r"""
    \s*(
        (?P<number>(?:\d+(?:\.\d*)?|\.\d+)) |
        (?P<ident>[A-Za-z_]\w*) |
        (?P<op>[\+\-\*/]) |
        (?P<lpar>\() |
        (?P<rpar>\))
    )
    """,
    re.VERBOSE,
)

@dataclass(frozen=True)
class Token:
    kind: str
    value: str

def _tokenize(s: str) -> List[Token]:
    pos = 0
    toks: List[Token] = []
    while pos < len(s):
        m = _TOKEN_RE.match(s, pos)
        if not m:
            raise ParseError(f"Unexpected character at position {pos}: {s[pos:pos+20]!r}")
        pos = m.end(0)
        if m.group("number") is not None:
            toks.append(Token("number", m.group("number")))
        elif m.group("ident") is not None:
            toks.append(Token("ident", m.group("ident")))
        elif m.group("op") is not None:
            toks.append(Token("op", m.group("op")))
        elif m.group("lpar") is not None:
            toks.append(Token("lpar", "("))
        elif m.group("rpar") is not None:
            toks.append(Token("rpar", ")"))
    return toks


class _Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.i = 0

    def _peek(self) -> Optional[Token]:
        return self.tokens[self.i] if self.i < len(self.tokens) else None

    def _eat(self, kind: str, value: str | None = None) -> Token:
        t = self._peek()
        if t is None:
            raise ParseError(f"Expected {kind} but reached end of input")
        if t.kind != kind:
            raise ParseError(f"Expected {kind} but got {t.kind} ({t.value!r})")
        if value is not None and t.value != value:
            raise ParseError(f"Expected {value!r} but got {t.value!r}")
        self.i += 1
        return t

    # Grammar (with precedence):
    # expr   := term (("+"|"-") term)*
    # term   := factor (("*"|"/") factor)*
    # factor := "-" factor | primary
    # primary:= number | ident | "(" expr ")"

    def parse_expr(self) -> Expr:
        node = self.parse_term()
        while True:
            t = self._peek()
            if t and t.kind == "op" and t.value in ("+", "-"):
                op = self._eat("op").value
                rhs = self.parse_term()
                node = (op, node, rhs)
            else:
                break
        return node

    def parse_term(self) -> Expr:
        node = self.parse_factor()
        while True:
            t = self._peek()
            if t and t.kind == "op" and t.value in ("*", "/"):
                op = self._eat("op").value
                rhs = self.parse_factor()
                node = (op, node, rhs)
            else:
                break
        return node

    def parse_factor(self) -> Expr:
        t = self._peek()
        if t and t.kind == "op" and t.value == "-":
            self._eat("op", "-")
            sub = self.parse_factor()
            return ("*", -1, sub)
        return self.parse_primary()

    def parse_primary(self) -> Expr:
        t = self._peek()
        if t is None:
            raise ParseError("Unexpected end of input")

        if t.kind == "number":
            raw = self._eat("number").value
            if "." in raw:
                return float(raw)
            return int(raw)

        if t.kind == "ident":
            return self._eat("ident").value

        if t.kind == "lpar":
            self._eat("lpar")
            node = self.parse_expr()
            self._eat("rpar")
            return node

        raise ParseError(f"Unexpected token: {t.kind} ({t.value!r})")


def parse(s: str) -> Expr:
    """Parse a string into an expression tree.

    Supports + - * /, parentheses, numbers, variables, and unary minus.
    """
    tokens = _tokenize(s)
    if not tokens:
        raise ParseError("Empty input")
    p = _Parser(tokens)
    node = p.parse_expr()
    if p._peek() is not None:
        t = p._peek()
        raise ParseError(f"Unexpected trailing token: {t.kind} ({t.value!r})")
    return node
