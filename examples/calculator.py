from expr_engine import parse, evaluate, simplify, differentiate, pretty

expr = parse("2*(x+1)")
print("tree:", expr)
print("pretty:", pretty(expr))
print("eval x=3:", evaluate(expr, {"x": 3}))

d = simplify(differentiate(expr, "x"))
print("d/dx:", pretty(d))
