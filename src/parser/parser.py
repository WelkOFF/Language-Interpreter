from src.lexer import token_
from src.ast.ast_ import *

LOWEST = 1
EQUALS = 2  # ==
LESSGREATER = 3  # > or <
SUM = 4  # +
PRODUCT = 5  # *
PREFIX = 6  # -X or !X
CALL = 7  # myFunction(X)
INDEX = 8  # array[index]

precedences = {
    token_.TokenType.EQ: EQUALS,
    token_.TokenType.NOT_EQ: EQUALS,
    token_.TokenType.LT: LESSGREATER,
    token_.TokenType.GT: LESSGREATER,
    token_.TokenType.PLUS: SUM,
    token_.TokenType.MINUS: SUM,
    token_.TokenType.SLASH: PRODUCT,
    token_.TokenType.ASTERISK: PRODUCT,
    token_.TokenType.LPAREN: CALL,
    token_.TokenType.LBRACKET: INDEX,
}


class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.errors = []

        self.cur_token = None
        self.peek_token = None
        self.next_token()
        self.next_token()

        # Parsing function maps
        self.prefix_parse_fns = {}
        self.infix_parse_fns = {}

        # Register prefix functions
        self.register_prefix(token_.TokenType.IDENT, self.parse_identifier)
        self.register_prefix(token_.TokenType.INT, self.parse_integer_literal)
        self.register_prefix(token_.TokenType.STRING, self.parse_string_literal)
        self.register_prefix(token_.TokenType.BANG, self.parse_prefix_expression)
        self.register_prefix(token_.TokenType.MINUS, self.parse_prefix_expression)
        self.register_prefix(token_.TokenType.TRUE, self.parse_boolean)
        self.register_prefix(token_.TokenType.FALSE, self.parse_boolean)
        self.register_prefix(token_.TokenType.LPAREN, self.parse_grouped_expression)
        self.register_prefix(token_.TokenType.IF, self.parse_if_expression)
        self.register_prefix(token_.TokenType.FUNCTION, self.parse_function_literal)
        self.register_prefix(token_.TokenType.LBRACKET, self.parse_array_literal)
        self.register_prefix(token_.TokenType.LBRACE, self.parse_hash_literal)

        # Register infix functions
        self.register_infix(token_.TokenType.PLUS, self.parse_infix_expression)
        self.register_infix(token_.TokenType.MINUS, self.parse_infix_expression)
        self.register_infix(token_.TokenType.SLASH, self.parse_infix_expression)
        self.register_infix(token_.TokenType.ASTERISK, self.parse_infix_expression)
        self.register_infix(token_.TokenType.EQ, self.parse_infix_expression)
        self.register_infix(token_.TokenType.NOT_EQ, self.parse_infix_expression)
        self.register_infix(token_.TokenType.LT, self.parse_infix_expression)
        self.register_infix(token_.TokenType.GT, self.parse_infix_expression)
        self.register_infix(token_.TokenType.LPAREN, self.parse_call_expression)
        self.register_infix(token_.TokenType.LBRACKET, self.parse_index_expression)

    def next_token(self):
        self.cur_token = self.peek_token
        self.peek_token = self.lexer.next_token()

    def cur_token_is(self, t):
        return self.cur_token.token_type == t

    def peek_token_is(self, t):
        return self.peek_token.token_type == t

    def expect_peek(self, t):
        if self.peek_token_is(t):
            self.next_token()
            return True
        else:
            self.peek_error(t)
            return False

    def errors(self):
        return self.errors

    def peek_error(self, t):
        msg = f"expected next token to be {t}, got {self.peek_token.token_type} instead"
        self.errors.append(msg)

    def no_prefix_parse_fn_error(self, t):
        msg = f"no prefix parse function for {t} found"
        self.errors.append(msg)

    def parse_program(self):
        program = Program()
        while self.cur_token.token_type != token_.TokenType.EOF:
            stmt = self.parse_statement()
            if stmt is not None:
                program.statements.append(stmt)
            self.next_token()
        return program

    def parse_identifier(self):
        return Identifier(token=self.cur_token, value=self.cur_token.literal)

    def parse_integer_literal(self):
        try:
            value = int(self.cur_token.literal)
            return IntegerLiteral(token=self.cur_token, value=value)
        except ValueError:
            msg = f"could not parse {self.cur_token.literal} as integer"
            self.errors.append(msg)
            return None

    def parse_string_literal(self):
        return StringLiteral(token=self.cur_token, value=self.cur_token.literal)

    def parse_prefix_expression(self):
        token = self.cur_token
        operator = self.cur_token.literal
        self.next_token()
        right = self.parse_expression(PREFIX)
        return PrefixExpression(token=token, operator=operator, right=right)

    def parse_infix_expression(self, left):
        token = self.cur_token
        operator = self.cur_token.literal
        precedence = self.cur_precedence()
        self.next_token()
        right = self.parse_expression(precedence)
        return InfixExpression(token=token, operator=operator, left=left, right=right)

    def parse_call_expression(self, function):
        token = self.cur_token
        arguments = self.parse_expression_list(token_.TokenType.RPAREN)
        return CallExpression(token=token, function=function, arguments=arguments)

    def parse_index_expression(self, left):
        token = self.cur_token
        self.next_token()
        index = self.parse_expression(LOWEST)
        if not self.expect_peek(token_.TokenType.RBRACKET):
            return None
        return IndexExpression(token=token, left=left, index=index)

    def parse_boolean(self):
        return Boolean(token=self.cur_token, value=self.cur_token_is(token_.TokenType.TRUE))

    def parse_grouped_expression(self):
        self.next_token()
        exp = self.parse_expression(LOWEST)
        if not self.expect_peek(token_.TokenType.RPAREN):
            return None
        return exp

    def parse_if_expression(self):
        token = self.cur_token
        if not self.expect_peek(token_.TokenType.LPAREN):
            return None
        self.next_token()
        condition = self.parse_expression(LOWEST)
        if not self.expect_peek(token_.TokenType.RPAREN):
            return None
        if not self.expect_peek(token_.TokenType.LBRACE):
            return None
        consequence = self.parse_block_statement()
        alternative = None
        if self.peek_token_is(token_.TokenType.ELSE):
            self.next_token()
            if not self.expect_peek(token_.TokenType.LBRACE):
                return None
            alternative = self.parse_block_statement()
        return IfExpression(token=token, condition=condition, consequence=consequence, alternative=alternative)

    def parse_function_literal(self):
        token = self.cur_token
        if not self.expect_peek(token_.TokenType.LPAREN):
            return None
        parameters = self.parse_function_parameters()
        if not self.expect_peek(token_.TokenType.LBRACE):
            return None
        body = self.parse_block_statement()
        return FunctionLiteral(token=token, parameters=parameters, body=body)

    def parse_function_parameters(self):
        identifiers = []
        if self.peek_token_is(token_.TokenType.RPAREN):
            self.next_token()
            return identifiers
        self.next_token()
        ident = Identifier(token=self.cur_token, value=self.cur_token.literal)
        identifiers.append(ident)
        while self.peek_token_is(token_.TokenType.COMMA):
            self.next_token()
            self.next_token()
            ident = Identifier(token=self.cur_token, value=self.cur_token.literal)
            identifiers.append(ident)
        if not self.expect_peek(token_.TokenType.RPAREN):
            return None
        return identifiers

    def parse_array_literal(self):
        token = self.cur_token
        elements = self.parse_expression_list(token_.TokenType.RBRACKET)
        return ArrayLiteral(token=token, elements=elements)

    def parse_expression_list(self, end):
        elements = []
        if self.peek_token_is(end):
            self.next_token()
            return elements
        self.next_token()
        elements.append(self.parse_expression(LOWEST))
        while self.peek_token_is(token_.TokenType.COMMA):
            self.next_token()
            self.next_token()
            elements.append(self.parse_expression(LOWEST))
        if not self.expect_peek(end):
            return None
        return elements

    def parse_hash_literal(self):
        token = self.cur_token
        pairs = {}
        while not self.peek_token_is(token_.TokenType.RBRACE):
            self.next_token()
            key = self.parse_expression(LOWEST)
            if not self.expect_peek(token_.TokenType.COLON):
                return None
            self.next_token()
            value = self.parse_expression(LOWEST)
            pairs[key] = value
            if not self.peek_token_is(token_.TokenType.RBRACE) and not self.expect_peek(token_.TokenType.COMMA):
                return None
        if not self.expect_peek(token_.TokenType.RBRACE):
            return None
        return HashLiteral(token=token, pairs=pairs)

    def parse_block_statement(self):
        token = self.cur_token
        statements = []
        self.next_token()
        while not self.cur_token_is(token_.TokenType.RBRACE) and not self.cur_token_is(token_.TokenType.EOF):
            stmt = self.parse_statement()
            if stmt is not None:
                statements.append(stmt)
            self.next_token()
        return BlockStatement(token=token, statements=statements)

    def parse_statement(self):
        if self.cur_token_is(token_.TokenType.LET):
            return self.parse_let_statement()
        elif self.cur_token_is(token_.TokenType.RETURN):
            return self.parse_return_statement()
        else:
            return self.parse_expression_statement()

    def parse_let_statement(self):
        token = self.cur_token
        if not self.expect_peek(token_.TokenType.IDENT):
            return None
        name = Identifier(token=self.cur_token, value=self.cur_token.literal)
        if not self.expect_peek(token_.TokenType.ASSIGN):
            return None
        self.next_token()
        value = self.parse_expression(LOWEST)
        if self.peek_token_is(token_.TokenType.SEMICOLON):
            self.next_token()
        return LetStatement(token=token, name=name, value=value)

    def parse_return_statement(self):
        token = self.cur_token
        self.next_token()
        value = self.parse_expression(LOWEST)
        if self.peek_token_is(token_.TokenType.SEMICOLON):
            self.next_token()
        return ReturnStatement(token=token, return_value=value)

    def parse_expression_statement(self):
        token = self.cur_token
        value = self.parse_expression(LOWEST)
        if self.peek_token_is(token_.TokenType.SEMICOLON):
            self.next_token()
        return ExpressionStatement(token=token, expression=value)

    def parse_expression(self, precedence):
        prefix = self.prefix_parse_fns[self.cur_token.token_type]
        if prefix is None:
            self.no_prefix_parse_fn_error(self.cur_token.token_type)
            return None
        left_exp = prefix()

        while not self.peek_token_is(token_.TokenType.SEMICOLON) and precedence < self.peek_precedence():
            infix = self.infix_parse_fns[self.peek_token.token_type]
            if infix is None:
                return left_exp
            self.next_token()
            left_exp = infix(left_exp)
        return left_exp

    def peek_precedence(self):
        if self.peek_token.token_type in precedences:
            return precedences[self.peek_token.token_type]
        return LOWEST

    def cur_precedence(self):
        if self.cur_token.token_type in precedences:
            return precedences[self.cur_token.token_type]
        return LOWEST

    def register_prefix(self, token_type, fn):
        self.prefix_parse_fns[token_type] = fn

    def register_infix(self, token_type, fn):
        self.infix_parse_fns[token_type] = fn
