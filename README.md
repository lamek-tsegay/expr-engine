# Expr Engine

A lightweight expression-tree engine for **parsing**, **evaluating**, **simplifying**, **pretty-printing**, and **symbolically differentiating** basic math expressions.

It represents expressions as:
- numbers (`int`/`float`)
- variables (`str`)
- composite nodes as a tuple: `(<op>, <left>, <right>)` where `<op>` is one of `+ - * /`

Example:

```python
from expr_engine import parse, evaluate, simplify, differentiate, pretty

expr = parse("2*(x+1)")
print(expr)                 # ('*', 2, ('+', 'x', 1))
print(pretty(expr))         # 2*(x+1)
print(evaluate(expr, {"x": 3}))  # 8

d = simplify(differentiate(expr, "x"))
print(pretty(d))            # 2
```

## Install (dev)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## CLI

```bash
expr "2*(x+1)" --x 5
expr "x*x + 3*x + 2" --diff x --x 10
```

## Why this matters

Expression trees are foundational in:
- compilers & interpreters
- calculators & symbolic algebra
- computational graphs in ML frameworks

## License

MIT
