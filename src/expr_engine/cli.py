from __future__ import annotations

import argparse
from typing import Dict

from . import parse, pretty, evaluate, simplify, differentiate


def _parse_env(pairs) -> Dict[str, float]:
    env: Dict[str, float] = {}
    for k, v in pairs:
        try:
            env[k] = float(v)
        except ValueError:
            raise SystemExit(f"Bad value for {k}: {v!r} (must be a number)")
    return env


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(prog="expr", description="Parse/evaluate/simplify/differentiate math expressions.")
    ap.add_argument("expr", help="Expression string, e.g. '2*(x+1)'")
    ap.add_argument("--simplify", action="store_true", help="Simplify the expression")
    ap.add_argument("--diff", metavar="VAR", help="Differentiate with respect to VAR")
    ap.add_argument("--pretty", action="store_true", help="Pretty-print the (final) expression")
    ap.add_argument("--eval", action="store_true", help="Evaluate the (final) expression")
    ap.add_argument("--var", action="append", nargs=2, default=[], metavar=("NAME", "VALUE"), help="Set variable, e.g. --var x 3")

    args = ap.parse_args(argv)
    env = _parse_env(args.var)

    expr = parse(args.expr)

    if args.diff:
        expr = differentiate(expr, args.diff)

    if args.simplify:
        expr = simplify(expr)

    # Default output behavior:
    # - if --eval: print number
    # - else if --pretty: print pretty string
    # - else: print raw tree
    if args.eval:
        out = evaluate(expr, env)
        print(out)
    elif args.pretty:
        print(pretty(expr))
    else:
        print(expr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
