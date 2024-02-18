import getpass
from src.repl.repl import start


def main():
    username = getpass.getuser()
    print(f"Hello {username}! This is the Monkey programming language!")
    print("Feel free to type in commands")
    start()


if __name__ == "__main__":
    main()
