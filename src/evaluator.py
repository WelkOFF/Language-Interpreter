from src import ast_
from src.environment import new_enclosed_environment
from src.object import Boolean, Null, Error, ReturnValue, Integer, String, Function, Array, HashPair, Hash, Builtin

NULL = Null()
TRUE = Boolean(True)
FALSE = Boolean(False)


class BuiltinFunction:
    def __init__(self, fn):
        self.fn = fn


def len_builtin(args):
    if len(args) != 1:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")

    if isinstance(args[0], Array):
        return Integer(len(args[0].elements))
    elif isinstance(args[0], String):
        return Integer(len(args[0].value))
    else:
        return new_error(f"argument to `len` not supported, got {args[0].type()}")


def puts_builtin(args):
    for arg in args:
        print(arg.inspect())
    return NULL


def first_builtin(args):
    if len(args) != 1:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")
    if not isinstance(args[0], Array):
        return new_error(f"argument to `first` must be ARRAY, got {args[0].type()}")

    if args[0].elements:
        return args[0].elements[0]
    return NULL


def last_builtin(args):
    if len(args) != 1:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")
    if not isinstance(args[0], Array):
        return new_error(f"argument to `last` must be ARRAY, got {args[0].type()}")

    if args[0].elements:
        return args[0].elements[-1]
    return NULL


def rest_builtin(args):
    if len(args) != 1:
        return new_error(f"wrong number of arguments. got={len(args)}, want=1")
    if not isinstance(args[0], Array):
        return new_error(f"argument to `rest` must be ARRAY, got {args[0].type()}")

    if args[0].elements:
        new_elements = args[0].elements[1:]
        return Array(new_elements)
    return NULL


def push_builtin(args):
    if len(args) != 2:
        return new_error(f"wrong number of arguments. got={len(args)}, want=2")
    if not isinstance(args[0], Array):
        return new_error(f"argument to `push` must be ARRAY, got {args[0].type()}")

    new_elements = args[0].elements + [args[1]]
    return Array(new_elements)


builtins = {
    "len": BuiltinFunction(len_builtin),
    "puts": BuiltinFunction(puts_builtin),
    "first": BuiltinFunction(first_builtin),
    "last": BuiltinFunction(last_builtin),
    "rest": BuiltinFunction(rest_builtin),
    "push": BuiltinFunction(push_builtin),
}


# Helper functions
def new_error(message):
    return Error(message)


def evaluate(node, env):
    # Statements
    if isinstance(node, ast_.Program):
        return eval_program(node, env)
    elif isinstance(node, ast_.BlockStatement):
        return eval_block_statement(node, env)
    elif isinstance(node, ast_.ExpressionStatement):
        return evaluate(node.expression, env)
    elif isinstance(node, ast_.ReturnStatement):
        val = evaluate(node.return_value, env)
        if is_error(val):
            return val
        return ReturnValue(val)
    elif isinstance(node, ast_.LetStatement):
        val = evaluate(node.value, env)
        if is_error(val):
            return val
        env.set(node.name.value, val)

    # Expressions
    elif isinstance(node, ast_.IntegerLiteral):
        return Integer(node.value)
    elif isinstance(node, ast_.StringLiteral):
        return String(node.value)
    elif isinstance(node, ast_.Boolean):
        return native_bool_to_boolean_object(node.value)
    elif isinstance(node, ast_.PrefixExpression):
        right = evaluate(node.right, env)
        if is_error(right):
            return right
        return eval_prefix_expression(node.operator, right)
    elif isinstance(node, ast_.InfixExpression):
        left = evaluate(node.left, env)
        if is_error(left):
            return left
        right = evaluate(node.right, env)
        if is_error(right):
            return right
        return eval_infix_expression(node.operator, left, right)
    elif isinstance(node, ast_.IfExpression):
        return eval_if_expression(node, env)
    elif isinstance(node, ast_.Identifier):
        return eval_identifier(node, env)
    elif isinstance(node, ast_.FunctionLiteral):
        params = node.parameters
        body = node.body
        return Function(params, env, body)
    elif isinstance(node, ast_.CallExpression):
        function = evaluate(node.function, env)
        if is_error(function):
            return function
        args = eval_expressions(node.arguments, env)
        if len(args) == 1 and is_error(args[0]):
            return args[0]
        return apply_function(function, args)
    elif isinstance(node, ast_.ArrayLiteral):
        elements = eval_expressions(node.elements, env)
        if len(elements) == 1 and is_error(elements[0]):
            return elements[0]
        return Array(elements)
    elif isinstance(node, ast_.IndexExpression):
        left = evaluate(node.left, env)
        if is_error(left):
            return left
        index = evaluate(node.index, env)
        if is_error(index):
            return index
        return eval_index_expression(left, index)
    elif isinstance(node, ast_.HashLiteral):
        return eval_hash_literal(node, env)

    return None


def eval_program(program, env):
    result = None
    for statement in program.statements:
        result = evaluate(statement, env)
        if isinstance(result, ReturnValue):
            return result.value
        elif isinstance(result, Error):
            return result
    return result


def eval_block_statement(block, env):
    result = None
    for statement in block.statements:
        result = evaluate(statement, env)
        if result is not None:
            rt = result.type()
            if rt in ("RETURN_VALUE", "ERROR"):
                return result
    return result


def native_bool_to_boolean_object(input):
    if input:
        return TRUE
    return FALSE


def eval_prefix_expression(operator, right):
    if operator == "!":
        return eval_bang_operator_expression(right)
    elif operator == "-":
        return eval_minus_prefix_operator_expression(right)
    return new_error(f"unknown operator: {operator}{right.type()}")


def eval_bang_operator_expression(right):
    if right == TRUE:
        return FALSE
    elif right == FALSE:
        return TRUE
    elif right == NULL:
        return TRUE
    else:
        return FALSE


def eval_minus_prefix_operator_expression(right):
    if right.type() != "INTEGER":
        return new_error(f"unknown operator: -{right.type()}")
    value = right.value
    return Integer(-value)


def eval_infix_expression(operator, left, right):
    if left.type() == "INTEGER" and right.type() == "INTEGER":
        return eval_integer_infix_expression(operator, left, right)
    elif left.type() == "STRING" and right.type() == "STRING":
        return eval_string_infix_expression(operator, left, right)
    elif operator == "==":
        return native_bool_to_boolean_object(left == right)
    elif operator == "!=":
        return native_bool_to_boolean_object(left != right)
    elif left.type() != right.type():
        return new_error(f"type mismatch: {left.type()} {operator} {right.type()}")
    else:
        return new_error(f"unknown operator: {left.type()} {operator} {right.type()}")


def eval_integer_infix_expression(operator, left, right):
    left_val = left.value
    right_val = right.value
    if operator == "+":
        return Integer(left_val + right_val)
    elif operator == "-":
        return Integer(left_val - right_val)
    elif operator == "*":
        return Integer(left_val * right_val)
    elif operator == "/":
        return Integer(left_val / right_val)
    elif operator == "<":
        return native_bool_to_boolean_object(left_val < right_val)
    elif operator == ">":
        return native_bool_to_boolean_object(left_val > right_val)
    elif operator == "==":
        return native_bool_to_boolean_object(left_val == right_val)
    elif operator == "!=":
        return native_bool_to_boolean_object(left_val != right_val)
    else:
        return new_error(f"unknown operator: {left.type()} {operator} {right.type()}")


def eval_string_infix_expression(operator, left, right):
    if operator != "+":
        return new_error(f"unknown operator: {left.type()} {operator} {right.type()}")
    return String(left.value + right.value)


def eval_expressions(exps, env):
    result = []
    for e in exps:
        evaluated = evaluate(e, env)
        if is_error(evaluated):
            return [evaluated]
        result.append(evaluated)
    return result


def eval_identifier(node, env):
    val = env.get(node.value)
    if val is not None:
        return val

    builtin = builtins.get(node.value)
    if builtin is not None:
        return builtin

    return new_error(f"identifier not found: {node.value}")


def eval_if_expression(ie, env):
    condition = evaluate(ie.condition, env)
    if is_error(condition):
        return condition
    if is_truthy(condition):
        return evaluate(ie.consequence, env)
    elif ie.alternative is not None:
        return evaluate(ie.alternative, env)
    else:
        return NULL


def eval_index_expression(left, index):
    if left.type() == "ARRAY" and index.type() == "INTEGER":
        return eval_array_index_expression(left, index)
    elif left.type() == "HASH":
        return eval_hash_index_expression(left, index)
    return new_error(f"index operator not supported: {left.type()}")


def eval_array_index_expression(array, index):
    idx = index.value
    max = len(array.elements) - 1
    if idx < 0 or idx > max:
        return NULL
    return array.elements[idx]


def eval_hash_index_expression(hash, index):
    if not isinstance(index, (String, Integer, Boolean)):
        return new_error(f"unusable as hash key: {index.type()}")
    pair = hash.pairs.get(index)
    if pair is None:
        return NULL
    return pair.value


def is_truthy(obj):
    if obj == NULL:
        return False
    elif obj == TRUE:
        return True
    elif obj == FALSE:
        return False
    else:
        return True


def apply_function(fn, args):
    if isinstance(fn, Function):
        extended_env = extend_function_env(fn, args)
        evaluated = evaluate(fn.body, extended_env)
        return unwrap_return_value(evaluated)
    elif isinstance(fn, Builtin):
        return fn.fn(*args)
    return new_error(f"not a function: {fn.type()}")


def extend_function_env(fn, args):
    env = new_enclosed_environment(fn.env)
    for i, param in enumerate(fn.parameters):
        env.set(param.value, args[i])
    return env


def unwrap_return_value(obj):
    if isinstance(obj, ReturnValue):
        return obj.value
    return obj


def eval_hash_literal(node, env):
    pairs = {}
    for key_node, value_node in node.pairs.items():
        key = evaluate(key_node, env)
        if is_error(key):
            return key
        value = evaluate(value_node, env)
        if is_error(value):
            return value
        hash_key = key
        pairs[hash_key] = HashPair(key, value)
    return Hash(pairs)


def new_error(msg):
    return Error(msg)


def is_error(obj):
    if obj is not None:
        return obj.type() == "ERROR"
    return False
