import getpass
import argparse

from src.repl.repl import start, start_with_file


def main():
    parser = argparse.ArgumentParser(description="Process a file.")
    parser.add_argument("file_path", type=str, nargs='?', help="The path to the file to process", default="none")

    args = parser.parse_args()
    if args.file_path != "none":
        start_with_file(args.file_path)
        return

    username = getpass.getuser()
    print(f"Hello {username}! This is the Monkey programming language!")
    print("Feel free to type in commands")
    start()


if __name__ == "__main__":
    main()
