from expr_engine import parse, pretty

def test_parse_precedence():
    e = parse("2+3*4")
    assert pretty(e) == "2+3*4"
    # should be 2 + (3*4)
    assert e == ("+", 2, ("*", 3, 4))

def test_parse_parentheses():
    e = parse("(2+3)*4")
    assert e == ("*", ("+", 2, 3), 4)

def test_unary_minus():
    e = parse("-x+1")
    # (-1*x)+1
    assert e == ("+", ("*", -1, "x"), 1)
