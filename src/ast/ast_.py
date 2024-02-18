from abc import ABC, abstractmethod
from typing import List


# Node and Expression Interfaces
class Node(ABC):
    @abstractmethod
    def token_literal(self) -> str:
        pass

    @abstractmethod
    def __str__(self) -> str:
        pass


class Statement(Node):
    @abstractmethod
    def statement_node(self):
        pass


class Expression(Node):
    @abstractmethod
    def expression_node(self):
        pass


# Program Class
class Program(Node):
    def __init__(self):
        self.statements: List[Statement] = []

    def token_literal(self) -> str:
        if self.statements:
            return self.statements[0].token_literal()
        else:
            return ""

    def __str__(self) -> str:
        return "".join(str(statement) for statement in self.statements)


# Statement Implementations
class LetStatement(Statement):
    def __init__(self, token, name, value):
        self.token = token
        self.name = name
        self.value = value

    def statement_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"{self.token_literal()} {str(self.name)} = {str(self.value)};"


class ReturnStatement(Statement):
    def __init__(self, token, return_value):
        self.token = token
        self.return_value = return_value

    def statement_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return_value_str = str(self.return_value) if self.return_value else ""
        return f"{self.token_literal()} {return_value_str};"


class ExpressionStatement(Statement):
    def __init__(self, token, expression):
        self.token = token
        self.expression = expression

    def statement_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return str(self.expression) if self.expression else ""


class BlockStatement(Statement):
    def __init__(self, token):
        self.token = token
        self.statements: List[Statement] = []

    def statement_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return "".join(str(statement) for statement in self.statements)


class Identifier(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.value


class Boolean(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return self.token.literal


class IntegerLiteral(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return str(self.value)


class PrefixExpression(Expression):
    def __init__(self, token, operator, right):
        self.token = token
        self.operator = operator
        self.right = right

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({self.operator}{str(self.right)})"


class InfixExpression(Expression):
    def __init__(self, token, left, operator, right):
        self.token = token
        self.left = left
        self.operator = operator
        self.right = right

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({str(self.left)} {self.operator} {str(self.right)})"


class IfExpression(Expression):
    def __init__(self, token, condition, consequence, alternative=None):
        self.token = token
        self.condition = condition
        self.consequence = consequence
        self.alternative = alternative

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        out = f"if {str(self.condition)} {str(self.consequence)}"
        if self.alternative:
            out += f" else {str(self.alternative)}"
        return out


class FunctionLiteral(Expression):
    def __init__(self, token, parameters, body):
        self.token = token
        self.parameters = parameters
        self.body = body

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        params = ", ".join([str(p) for p in self.parameters])
        return f"{self.token_literal()}({params}) {str(self.body)}"


class CallExpression(Expression):
    def __init__(self, token, function, arguments):
        self.token = token
        self.function = function
        self.arguments = arguments

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        args = ", ".join([str(a) for a in self.arguments])
        return f"{str(self.function)}({args})"


class StringLiteral(Expression):
    def __init__(self, token, value):
        self.token = token
        self.value = value

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f'"{self.value}"'


class ArrayLiteral(Expression):
    def __init__(self, token, elements):
        self.token = token
        self.elements = elements

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        elements = ", ".join([str(e) for e in self.elements])
        return f"[{elements}]"


class IndexExpression(Expression):
    def __init__(self, token, left, index):
        self.token = token
        self.left = left
        self.index = index

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        return f"({str(self.left)}[{str(self.index)}])"


class HashLiteral(Expression):
    def __init__(self, token, pairs):
        self.token = token
        # Ensure pairs is a dict with Expression keys and Expression values
        self.pairs = pairs

    def expression_node(self):
        pass

    def token_literal(self) -> str:
        return self.token.literal

    def __str__(self) -> str:
        pairs = ", ".join([f"{str(key)}:{str(value)}" for key, value in self.pairs.items()])
        return f"{{{pairs}}}"
