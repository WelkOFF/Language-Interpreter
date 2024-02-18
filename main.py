import getpass
import argparse

from src.repl.repl import start, start_with_file


def greet_user():
    username = getpass.getuser()
    print(f"Hello {username}! This is the Monkey programming language!")
    print("Feel free to type in commands")


def get_for_file_input():
    parser = argparse.ArgumentParser(description="Process a file.")
    parser.add_argument("file_path", type=str, nargs='?', help="The path to the file to process", default="none")

    args = parser.parse_args()
    return args.file_path


def main():
    file_path = get_for_file_input()
    file_mode = file_path != "none"
    if file_mode:
        print(file_path + " output:")
        start_with_file(file_path)
        return
    else:
        greet_user()
        start()


if __name__ == "__main__":
    main()
