from src.lexer import Lexer
from src.parser import Parser


def test_let_statements():
    tests = [
        {"input": "let x = 5;", "expected_identifier": "x", "expected_value": 5},
        {"input": "let y = true;", "expected_identifier": "y", "expected_value": True},
        {"input": "let foobar = y;", "expected_identifier": "foobar", "expected_value": "y"},
    ]

    for tt in tests:
        lexer = Lexer(tt["input"])
        parser = Parser(lexer)
        program = parser.parse_program()
        check_parser_errors(parser)

        assert len(program.statements) == 1, f"program should contain 1 statement. got={len(program.statements)}"

        stmt = program.statements[0]
        test_let_statement(stmt, tt["expected_identifier"])

        val = stmt.value
        test_literal_expression(val, tt["expected_value"])


def test_let_statement(stmt, name):
    assert stmt.token_literal() == "let", f"stmt.token_literal not 'let'. got={stmt.token_literal()}"
    assert stmt.name.value == name, f"stmt.name.value not '{name}'. got={stmt.name.value}"
    assert stmt.name.token_literal() == name, f"stmt.name.token_literal not '{name}'. got={stmt.name.token_literal()}"


def test_literal_expression(exp, expected):
    if isinstance(expected, bool):
        test_boolean_literal(exp, expected)
    elif isinstance(expected, int):
        test_integer_literal(exp, expected)
    elif isinstance(expected, str):
        test_identifier(exp, expected)
    else:
        assert False, f"Type of exp not handled. got={exp}"


def test_integer_literal(il, value):
    assert il.value == value, f"il.value not {value}. got={il.value}"
    assert il.token_literal() == str(value), f"il.token_literal not {value}. got={il.token_literal()}"


def test_boolean_literal(bl, value):
    assert bl.value == value, f"bl.value not {value}. got={bl.value}"
    assert bl.token_literal() == str(value).lower(), f"bl.token_literal not {value}. got={bl.token_literal()}"


def test_identifier(exp, value):
    assert exp.value == value, f"exp.value not {value}. got={exp.value}"
    assert exp.token_literal() == value, f"exp.token_literal not {value}. got={exp.token_literal()}"


def test_return_statements():
    tests = [
        {"input": "return 5;", "expected_value": 5},
        {"input": "return true;", "expected_value": True},
        {"input": "return foobar;", "expected_value": "foobar"},
    ]

    for tt in tests:
        lexer = Lexer(tt["input"])
        parser = Parser(lexer)
        program = parser.parse_program()
        check_parser_errors(parser)

        assert len(program.statements) == 1, f"program should contain 1 statement. got={len(program.statements)}"

        stmt = program.statements[0]
        assert stmt.token_literal() == "return", f"stmt.token_literal not 'return'. got={stmt.token_literal()}"

        val = stmt.return_value
        test_literal_expression(val, tt["expected_value"])


def test_identifier_expression():
    input_ = "foobar;"

    lexer = Lexer(input_)
    parser = Parser(lexer)
    program = parser.parse_program()
    check_parser_errors(parser)

    assert len(program.statements) == 1, f"program has not enough statements. got={len(program.statements)}"

    stmt = program.statements[0]
    assert stmt.token_literal() == "foobar", f"stmt.token_literal not 'foobar'. got={stmt.token_literal()}"


def test_integer_literal_expression():
    input_ = "5;"

    lexer = Lexer(input_)
    parser = Parser(lexer)
    program = parser.parse_program()
    check_parser_errors(parser)

    assert len(program.statements) == 1, f"program has not enough statements. got={len(program.statements)}"

    stmt = program.statements[0]
    assert stmt.token_literal() == "5", f"stmt.token_literal not '5'. got={stmt.token_literal()}"


def test_boolean_literal_expression():
    input_ = "true;"

    lexer = Lexer(input_)
    parser = Parser(lexer)
    program = parser.parse_program()
    check_parser_errors(parser)

    assert len(program.statements) == 1, f"program has not enough statements. got={len(program.statements)}"

    stmt = program.statements[0]
    assert stmt.token_literal() == "true", f"stmt.token_literal not 'true'. got={stmt.token_literal()}"


def test_prefix_expression():
    tests = [
        {"input": "!5;", "operator": "!", "value": 5},
        {"input": "-15;", "operator": "-", "value": 15},
        {"input": "!foobar;", "operator": "!", "value": "foobar"},
        {"input": "-foobar;", "operator": "-", "value": "foobar"},
        {"input": "!true;", "operator": "!", "value": True},
        {"input": "!false;", "operator": "!", "value": False},
    ]

    for tt in tests:
        lexer = Lexer(tt["input"])
        parser = Parser(lexer)
        program = parser.parse_program()
        check_parser_errors(parser)

        assert len(program.statements) == 1, f"program has not enough statements. got={len(program.statements)}"

        stmt = program.statements[0]
        exp = stmt.expression
        assert exp.operator == tt["operator"], f"exp.operator not '{tt['operator']}'. got={exp.operator}"

        test_literal_expression(exp.right, tt["value"])


def test_infix_expressions():
    tests = [
        {"input": "5 + 5;", "left_value": 5, "operator": "+", "right_value": 5},
        {"input": "5 - 5;", "left_value": 5, "operator": "-", "right_value": 5},
        {"input": "5 * 5;", "left_value": 5, "operator": "*", "right_value": 5},
        {"input": "5 / 5;", "left_value": 5, "operator": "/", "right_value": 5},
        {"input": "5 > 5;", "left_value": 5, "operator": ">", "right_value": 5},
        {"input": "5 < 5;", "left_value": 5, "operator": "<", "right_value": 5},
        {"input": "5 == 5;", "left_value": 5, "operator": "==", "right_value": 5},
        {"input": "5 != 5;", "left_value": 5, "operator": "!=", "right_value": 5},
        {"input": "true == true", "left_value": True, "operator": "==", "right_value": True},
        {"input": "true != false", "left_value": True, "operator": "!=", "right_value": False},
        {"input": "false == false", "left_value": False, "operator": "==", "right_value": False},
        {"input": "foobar + barfoo", "left_value": "foobar", "operator": "+", "right_value": "barfoo"},
        {"input": "foobar - barfoo", "left_value": "foobar", "operator": "-", "right_value": "barfoo"},
    ]

    for tt in tests:
        lexer = Lexer(tt["input"])
        parser = Parser(lexer)
        program = parser.parse_program()
        check_parser_errors(parser)

        assert len(program.statements) == 1, f"program has not enough statements. got={len(program.statements)}"

        stmt = program.statements[0]
        exp = stmt.expression
        test_infix_expression(exp, tt["left_value"], tt["operator"], tt["right_value"])


def test_infix_expression(exp, left, operator, right):
    assert exp.operator == operator, f"exp.operator not '{operator}'. got={exp.operator}"
    test_literal_expression(exp.left, left)
    test_literal_expression(exp.right, right)


def test_operator_precedence_parsing():
    tests = [
        {"input": "-a * b", "expected": "((-a) * b)"},
        {"input": "!-a", "expected": "(!(-a))"},
        {"input": "a + b + c", "expected": "((a + b) + c)"},
        {"input": "a + b - c", "expected": "((a + b) - c)"},
        {"input": "a * b * c", "expected": "((a * b) * c)"},
        {"input": "a * b / c", "expected": "((a * b) / c)"},
        {"input": "a + b / c", "expected": "(a + (b / c))"},
        {"input": "a + b * c + d / e - f", "expected": "(((a + (b * c)) + (d / e)) - f)"},
        {"input": "3 + 4; -5 * 5", "expected": "(3 + 4)((-5) * 5)"},
        {"input": "5 > 4 == 3 < 4", "expected": "((5 > 4) == (3 < 4))"},
        {"input": "5 < 4 != 3 > 4", "expected": "((5 < 4) != (3 > 4))"},
        {"input": "3 + 4 * 5 == 3 * 1 + 4 * 5", "expected": "((3 + (4 * 5)) == ((3 * 1) + (4 * 5)))"},
        {"input": "true", "expected": "true"},
        {"input": "false", "expected": "false"},
        {"input": "3 > 5 == false", "expected": "((3 > 5) == false)"},
        {"input": "3 < 5 == true", "expected": "((3 < 5) == true)"},
        {"input": "1 + (2 + 3) + 4", "expected": "((1 + (2 + 3)) + 4)"},
        {"input": "(5 + 5) * 2", "expected": "((5 + 5) * 2)"},
        {"input": "2 / (5 + 5)", "expected": "(2 / (5 + 5))"},
    ]

    for tt in tests:
        lexer = Lexer(tt["input"])
        parser = Parser(lexer)
        program = parser.parse_program()
        check_parser_errors(parser)

        actual = str(program)
        assert actual == tt["expected"], f'expected={tt["expected"]}, got={actual}'


def test_if_expression():
    input_ = "if (x < y) { x }"

    lexer = Lexer(input_)
    parser = Parser(lexer)
    program = parser.parse_program()
    check_parser_errors(parser)

    assert len(program.statements) == 1, f"program has not enough statements. got={len(program.statements)}"

    stmt = program.statements[0]
    assert stmt.token_literal() == "if", f"stmt.token_literal not 'if'. got={stmt.token_literal()}"

    exp = stmt.expression
    assert exp.token_literal() == "(", f"exp.token_literal not '('. got={exp.token_literal()}"

    exp = stmt.consequence
    assert exp.token_literal() == "{", f"exp.token_literal not '{{'. got={exp.token_literal()}"

    assert len(exp.statements) == 1, f"consequence is not 1 statement. got={len(exp.statements)}"

    stmt = exp.statements[0]
    assert stmt.token_literal() == "x", f"stmt.token_literal not 'x'. got={stmt.token_literal()}"


def check_parser_errors(parser):
    errors = parser.errors
    if not errors:
        return

    assert False, f"Parser has {len(errors)} errors:\n" + "\n".join(f"parser error: {msg}" for msg in errors)
