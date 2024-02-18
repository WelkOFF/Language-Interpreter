import sys

PROMPT = ">> "


def start(in_stream=sys.stdin, out_stream=sys.stdout):
    from environment import Environment
    from lexer import Lexer
    from parser import Parser
    from evaluator import evaluate

    env = Environment()

    while True:
        out_stream.write(PROMPT)
        out_stream.flush()
        line = in_stream.readline()
        if not line:
            break  # EOF or Ctrl-D

        lexer = Lexer(line)
        parser = Parser(lexer)

        program = parser.parse_program()
        if parser.errors:
            print_parser_errors(out_stream, parser.errors)
            continue

        evaluated = evaluate(program, env)
        if evaluated is not None:
            out_stream.write(evaluated.inspect() + '\n')


def print_parser_errors(out_stream, errors):
    out_stream.write("Woops! We ran into some monkey business here!\n")
    out_stream.write(" parser errors:\n")
    for msg in errors:
        out_stream.write("\t" + msg + "\n")


if __name__ == "__main__":
    start()
