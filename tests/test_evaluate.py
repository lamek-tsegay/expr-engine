import pytest
from expr_engine import parse, evaluate

def test_evaluate():
    e = parse("2*(x+1)")
    assert evaluate(e, {"x": 3}) == 8

def test_missing_var():
    e = parse("x+1")
    with pytest.raises(KeyError):
        evaluate(e, {})
