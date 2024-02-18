# Assuming the necessary imports or definitions of Program, LetStatement, Identifier, Token, and TokenType
from src.lexer.token_ import Token, TokenType


def test_string():
    program = Program()
    program.statements = [
        LetStatement(
            token=Token(token_type=TokenType.LET, literal="let"),
            name=Identifier(
                token=Token(token_type=TokenType.IDENT, literal="myVar"),
                value="myVar"
            ),
            value=Identifier(
                token=Token(token_type=TokenType.IDENT, literal="anotherVar"),
                value="anotherVar"
            )
        )
    ]

    assert str(program) == "let myVar = anotherVar;"

