import hashlib

NULL_OBJ = "NULL"
ERROR_OBJ = "ERROR"
INTEGER_OBJ = "INTEGER"
BOOLEAN_OBJ = "BOOLEAN"
STRING_OBJ = "STRING"
RETURN_VALUE_OBJ = "RETURN_VALUE"
FUNCTION_OBJ = "FUNCTION"
BUILTIN_OBJ = "BUILTIN"
ARRAY_OBJ = "ARRAY"
HASH_OBJ = "HASH"


class Object:
    def type(self):
        raise NotImplementedError

    def inspect(self):
        raise NotImplementedError


class Hashable(Object):
    def hash_key(self):
        raise NotImplementedError


class Integer(Hashable):
    def __init__(self, value):
        self.value = value

    def type(self):
        return INTEGER_OBJ

    def inspect(self):
        return str(self.value)

    def hash_key(self):
        return self.type(), self.value


class Boolean(Hashable):
    def __init__(self, value):
        self.value = value

    def type(self):
        return BOOLEAN_OBJ

    def inspect(self):
        return str(self.value).lower()

    def hash_key(self):
        value = 1 if self.value else 0
        return self.type(), value


class Null(Object):
    def type(self):
        return NULL_OBJ

    def inspect(self):
        return "null"


class ReturnValue(Object):
    def __init__(self, value):
        self.value = value

    def type(self):
        return RETURN_VALUE_OBJ

    def inspect(self):
        return self.value.inspect()


class Error(Object):
    def __init__(self, message):
        self.message = message

    def type(self):
        return ERROR_OBJ

    def inspect(self):
        return f"ERROR: {self.message}"


class Function(Object):
    def __init__(self, parameters, body, env):
        self.parameters = parameters
        self.body = body
        self.env = env

    def type(self):
        return FUNCTION_OBJ

    def inspect(self):
        params = ", ".join([p.string() for p in self.parameters])
        return f"fn({params}) {{\n{str(self.body)}\n}}"


class String(Hashable):
    def __init__(self, value):
        self.value = value

    def type(self):
        return STRING_OBJ

    def inspect(self):
        return self.value

    def hash_key(self):
        h = hashlib.sha256(self.value.encode())
        return self.type(), int(h.hexdigest(), 16)


class Builtin(Object):
    def __init__(self, fn):
        self.fn = fn

    def type(self):
        return BUILTIN_OBJ

    def inspect(self):
        return "builtin function"


class Array(Object):
    def __init__(self, elements):
        self.elements = elements

    def type(self):
        return ARRAY_OBJ

    def inspect(self):
        elements = [str(e.inspect()) for e in self.elements]
        return f"[{', '.join(elements)}]"


class HashPair(Object):
    def __init__(self, key, value):
        self.key = key
        self.value = value

    def inspect(self):
        return f"{self.key.inspect()}: {self.value.inspect()}"


class Hash(Object):
    def __init__(self, pairs):
        self.pairs = pairs

    def type(self):
        return HASH_OBJ

    def inspect(self):
        pairs = [p.inspect() for p in self.pairs]
        return f"{{{', '.join(pairs)}}}"
