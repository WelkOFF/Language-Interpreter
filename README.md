# Monkey Programming Language Interpreter

Welcome to the Monkey programming language interpreter project! Monkey is a small, dynamically typed programming language designed for simplicity and learning. This interpreter is written in Python and allows you to execute Monkey programming language scripts and interact with the language through a Read-Eval-Print Loop (REPL).

## Features

- **Variables**: Support for binding values to names.
- **Data Types**: Includes integers, booleans, strings, arrays, and hash maps.
- **Functions**: First-class and higher-order functions with closures.
- **Control Structures**: Conditionals (`if` statements) and return statements for controlling flow.
- **Built-in Functions**: A small set of built-in functions for common operations.
- **REPL**: An interactive shell to execute Monkey language expressions and statements.

## Getting Started

### Prerequisites

Ensure you have Python 3.6 or later installed on your machine. You can verify your Python version by running:

Running the REPL
To start the Monkey REPL, run the following command in the terminal:
```bash
python repl.py
```

You should see the prompt >> indicating that the REPL is ready to accept input. Try typing some Monkey code:

```bash
>> let add = fn(x, y) { return x + y; };
>> add(5, 5);
```

## Examples
Here are some examples of what you can do with Monkey:

## Variables and Functions

```bash
let name = "Monkey";
let greet = fn(name) { return "Hello, " + name + "!"; };
greet(name);
```

## Factorial Function

```bash
let arr = [1, 2, 3, 4, 5];
let sumArray = fn(array) {
    let sum = 0;
    for (let i = 0; i < len(array); i = i + 1) {
        sum = sum + array[i];
    }
    return sum;
};
sumArray(arr);

let map = {"name": "Monkey", "age": 7};
map["name"];
```

## Command Line Mode
```bash
python3 main.py
```

## File Interpreter Mode

```bash
python3 main.py filename1
```
