from src.token_ import Token, TokenType


class Lexer:
    def __init__(self, input: str):
        self.input = input
        self.position = 0
        self.read_position = 0
        self.ch = ''
        self.read_char()

    def read_char(self):
        if self.read_position >= len(self.input):
            self.ch = '\0'  # Use '\0' as EOF symbol in Python
        else:
            self.ch = self.input[self.read_position]
        self.position = self.read_position
        self.read_position += 1

    def peek_char(self):
        if self.read_position >= len(self.input):
            return '\0'
        else:
            return self.input[self.read_position]

    def skip_whitespace(self):
        while self.ch in (' ', '\t', '\n', '\r'):
            self.read_char()

    def read_identifier(self):
        start_position = self.position
        while self.ch.isalpha() or self.ch == '_':
            self.read_char()
        return self.input[start_position:self.position]

    def read_number(self):
        start_position = self.position
        while self.ch.isdigit():
            self.read_char()
        return self.input[start_position:self.position]

    def read_string(self):
        start_position = self.position + 1
        while True:
            self.read_char()
            if self.ch == '"' or self.ch == '\0':
                break
        return self.input[start_position:self.position]

    def next_token(self):
        self.skip_whitespace()
        if self.ch == '=':
            if self.peek_char() == '=':
                self.read_char()
                tok = Token(TokenType.EQ, '==')
            else:
                tok = Token(TokenType.ASSIGN, '=')
        elif self.ch == '+':
            tok = Token(TokenType.PLUS, '+')
        elif self.ch == '-':
            tok = Token(TokenType.MINUS, '-')
        elif self.ch == '!':
            if self.peek_char() == '=':
                self.read_char()
                tok = Token(TokenType.NOT_EQ, '!=')
            else:
                tok = Token(TokenType.BANG, '!')
        elif self.ch == '/':
            tok = Token(TokenType.SLASH, '/')
        elif self.ch == '*':
            tok = Token(TokenType.ASTERISK, '*')
        elif self.ch == '<':
            tok = Token(TokenType.LT, '<')
        elif self.ch == '>':
            tok = Token(TokenType.GT, '>')
        elif self.ch == ';':
            tok = Token(TokenType.SEMICOLON, ';')
        elif self.ch == ':':
            tok = Token(TokenType.COLON, ':')
        elif self.ch == ',':
            tok = Token(TokenType.COMMA, ',')
        elif self.ch == '{':
            tok = Token(TokenType.LBRACE, '{')
        elif self.ch == '}':
            tok = Token(TokenType.RBRACE, '}')
        elif self.ch == '(':
            tok = Token(TokenType.LPAREN, '(')
        elif self.ch == ')':
            tok = Token(TokenType.RPAREN, ')')
        elif self.ch == '"':
            tok = Token(TokenType.STRING, self.read_string())
        elif self.ch == '[':
            tok = Token(TokenType.LBRACKET, '[')
        elif self.ch == ']':
            tok = Token(TokenType.RBRACKET, ']')
        elif self.ch == '\x00':
            tok = Token(TokenType.EOF, '')
        else:
            if self.ch.isalpha() or self.ch == '_':
                literal = self.read_identifier()
                token_type = self.lookup_ident(literal)
                tok = Token(token_type, literal)
                return tok
            elif self.ch.isdigit():
                literal = self.read_number()
                tok = Token(TokenType.INT, literal)
                return tok
            else:
                tok = Token(TokenType.ILLEGAL, self.ch)

        self.read_char()
        return tok

    def lookup_ident(self, ident):
        # Define the lookup table for keywords
        keywords = {
            "fn": TokenType.FUNCTION,
            "let": TokenType.LET,
            "true": TokenType.TRUE,
            "false": TokenType.FALSE,
            "if": TokenType.IF,
            "else": TokenType.ELSE,
            "return": TokenType.RETURN,
        }
        return keywords.get(ident, TokenType.IDENT)