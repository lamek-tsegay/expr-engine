# Expr Engine

A lightweight expression-tree engine for **parsing**, **evaluating**, **simplifying**, **pretty-printing**, and **symbolically differentiating** mathematical expressions.

Expr Engine represents expressions using recursive expression trees, a structure widely used in compilers, interpreters, and symbolic math systems.

---

## Features

* Parse mathematical expressions into expression trees
* Evaluate expressions with variable substitution
* Simplify expressions through algebraic rules and constant folding
* Pretty-print expressions in readable mathematical form
* Perform symbolic differentiation

Supported operators:

```
+   addition
-   subtraction
*   multiplication
/   division
```

---

## Expression Representation

Expressions are represented as:

* **numbers** → `int` or `float`
* **variables** → `str`
* **compound expressions** → tuples

```
(<operator>, <left>, <right>)
```

Example:

```
('*', 2, ('+', 'x', 1))
```

represents the expression:

```
2 * (x + 1)
```

---

## Example Usage

```python
from expr_engine import parse, evaluate, simplify, differentiate, pretty

expr = parse("2*(x+1)")

print(expr)
# ('*', 2, ('+', 'x', 1))

print(pretty(expr))
# 2*(x+1)

print(evaluate(expr, {"x": 3}))
# 8

d = simplify(differentiate(expr, "x"))
print(pretty(d))
# 2
```

---

## Installation (Development)

Clone the repository and install locally.

```bash
git clone https://github.com/lamek-tsegay/expr-engine.git
cd expr-engine

python -m venv .venv
source .venv/bin/activate

pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

---

## Command Line Interface

Expr Engine includes a CLI calculator.

Evaluate an expression:

```
expr "2*(x+1)" --x 5
```

Differentiate an expression:

```
expr "x*x + 3*x + 2" --diff x --x 10
```

Example output:

```
2*x + 3
```

---

## Project Structure

```
expr-engine
│
├── src/expr_engine
│   ├── parser.py
│   ├── evaluate.py
│   ├── simplify.py
│   ├── differentiate.py
│   ├── pretty.py
│   └── cli.py
│
├── tests
│   ├── test_parser.py
│   ├── test_evaluate.py
│   └── test_simplify.py
│
└── pyproject.toml
```

---

## Why This Project Matters

Expression trees are foundational in many areas of computer science, including:

* **compilers and interpreters**
* **symbolic algebra systems**
* **calculators and computer algebra software**
* **computational graphs used in machine learning frameworks**

Projects like this demonstrate core concepts such as:

* recursion
* tree data structures
* parsing
* symbolic computation

---

## Future Improvements

Planned enhancements include:

* exponentiation operator (`^`)
* support for functions (`sin`, `log`, `exp`)
* additional simplification rules
* LaTeX export for expressions
* expanded differentiation support

---

## License

MIT License
