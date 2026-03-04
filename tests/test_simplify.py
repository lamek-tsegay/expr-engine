from expr_engine import parse, simplify, pretty, differentiate

def test_simplify_identities():
    assert simplify(parse("x+0")) == "x"
    assert simplify(parse("0+x")) == "x"
    assert simplify(parse("x*1")) == "x"
    assert simplify(parse("1*x")) == "x"
    assert simplify(parse("x*0")) == 0

def test_simplify_constant_folding():
    assert simplify(parse("2*(3+1)")) == 8

def test_differentiate_and_simplify():
    expr = parse("x*x + 3*x + 2")
    d = simplify(differentiate(expr, "x"))
    # derivative is 2*x + 3
    assert pretty(d) in ("2*x+3", "3+2*x")
