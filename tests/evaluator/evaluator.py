from src.evaluator import evaluator
from src.lexer.lexer import Lexer
from src.object.environment import Environment
from src.object.object import Object
from src.parser.parser import Parser


def test_eval_integer_expression():
    tests = [
        {"input": "5", "expected": 5},
        {"input": "10", "expected": 10},
        {"input": "-5", "expected": -5},
        {"input": "-10", "expected": -10},
        {"input": "5 + 5 + 5 + 5 - 10", "expected": 10},
        {"input": "2 * 2 * 2 * 2 * 2", "expected": 32},
        {"input": "-50 + 100 + -50", "expected": 0},
        {"input": "5 * 2 + 10", "expected": 20},
        {"input": "5 + 2 * 10", "expected": 25},
        {"input": "20 + 2 * -10", "expected": 0},
        {"input": "50 / 2 * 2 + 10", "expected": 60},
        {"input": "2 * (5 + 10)", "expected": 30},
        {"input": "3 * 3 * 3 + 10", "expected": 37},
        {"input": "3 * (3 * 3) + 10", "expected": 37},
        {"input": "(5 + 10 * 2 + 15 / 3) * 2 + -10", "expected": 50},
    ]

    for tt in tests:
        evaluated = test_eval(tt["input"])
        test_integer_object(evaluated, tt["expected"])


def test_eval_boolean_expression():
    tests = [
        {"input": "true", "expected": True},
        {"input": "false", "expected": False},
        {"input": "1 < 2", "expected": True},
        {"input": "1 > 2", "expected": False},
        {"input": "1 < 1", "expected": False},
        {"input": "1 > 1", "expected": False},
        {"input": "1 == 1", "expected": True},
        {"input": "1 != 1", "expected": False},
        {"input": "1 == 2", "expected": False},
        {"input": "1 != 2", "expected": True},
        {"input": "true == true", "expected": True},
        {"input": "false == false", "expected": True},
        {"input": "true == false", "expected": False},
        {"input": "true != false", "expected": True},
        {"input": "false != true", "expected": True},
        {"input": "(1 < 2) == true", "expected": True},
        {"input": "(1 < 2) == false", "expected": False},
        {"input": "(1 > 2) == true", "expected": False},
        {"input": "(1 > 2) == false", "expected": True},
    ]

    for tt in tests:
        evaluated = test_eval(tt["input"])
        assert evaluated is not None, f"object is None"
        assert evaluated.value == tt[
            "expected"], f"object has wrong value. got={evaluated.value}, want={tt['expected']}"


def test_bang_operator():
    tests = [
        {"input": "!true", "expected": False},
        {"input": "!false", "expected": True},
        {"input": "!5", "expected": False},
        {"input": "!!true", "expected": True},
        {"input": "!!false", "expected": False},
        {"input": "!!5", "expected": True},
    ]

    for tt in tests:
        evaluated = test_eval(tt["input"])
        assert evaluated is not None, f"object is None"
        assert evaluated.value == tt[
            "expected"], f"object has wrong value. got={evaluated.value}, want={tt['expected']}"


def test_if_else_expressions():
    tests = [
        {"input": "if (true) { 10 }", "expected": 10},
        {"input": "if (false) { 10 }", "expected": None},
        {"input": "if (1) { 10 }", "expected": 10},
        {"input": "if (1 < 2) { 10 }", "expected": 10},
        {"input": "if (1 > 2) { 10 }", "expected": None},
        {"input": "if (1 > 2) { 10 } else { 20 }", "expected": 20},
        {"input": "if (1 < 2) { 10 } else { 20 }", "expected": 10},
    ]

    for tt in tests:
        evaluated = test_eval(tt["input"])
        if tt["expected"] is None:
            assert evaluated is not None, f"object is None"
        else:
            test_integer_object(evaluated, tt["expected"])


def test_function_object():
    input_ = "fn(x) { x + 2; };"
    evaluated = test_eval(input_)
    assert evaluated is not None, f"object is None"


def test_function_application():
    tests = [
        {"input": "let identity = fn(x) { x; }; identity(5);", "expected": 5},
        {"input": "let identity = fn(x) { return x; }; identity(5);", "expected": 5},
        {"input": "let double = fn(x) { x * 2; }; double(5);", "expected": 10},
        {"input": "let add = fn(x, y) { x + y; }; add(5, 5);", "expected": 10},
        {"input": "let add = fn(x, y) { x + y; }; add(5 + 5, add(5, 5));", "expected": 20},
        {"input": "fn(x) { x; }(5)", "expected": 5},
    ]

    for tt in tests:
        evaluated = test_eval(tt["input"])
        test_integer_object(evaluated, tt["expected"])


def test_eval(input_: str) -> Object:
    lexer = Lexer(input_)
    parser = Parser(lexer)
    program = parser.parse_program()
    env = Environment()
    return evaluator.evaluate(program, env)


def test_integer_object(obj: Object, expected: int):
    assert obj is not None, f"object is None"
    assert obj.value == expected, f"object has wrong value. got={obj.value}, want={expected}"
