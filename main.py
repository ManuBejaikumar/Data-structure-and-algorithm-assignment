import re
from pathlib import Path


class Stack:
    """A simple last-in, first-out (LIFO) stack."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack.")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Cannot peek at an empty stack.")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def size(self):
        return len(self._items)


OPERATORS = {
    "+": (1, "left"),
    "-": (1, "left"),
    "*": (2, "left"),
    "/": (2, "left"),
}
TOKEN_PATTERN = re.compile(r"\d+(?:\.\d+)?|[()+\-*/]")


def tokenize(expression):
    """Convert an expression into tokens and reject unknown characters."""
    tokens = []
    position = 0
    while position < len(expression):
        if expression[position].isspace():
            position += 1
            continue
        match = TOKEN_PATTERN.match(expression, position)
        if not match:
            raise ValueError(
                f"Unexpected character {expression[position]!r} at position {position + 1}"
            )
        tokens.append(match.group())
        position = match.end()
    if not tokens:
        raise ValueError("Expression is empty.")
    return tokens


def to_postfix(tokens):
    """Use the shunting-yard algorithm to convert infix tokens to postfix."""
    output = []
    operators = Stack()
    expect_operand = True

    for token in tokens:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            if not expect_operand:
                raise ValueError("Missing operator between numbers.")
            output.append(token)
            expect_operand = False

        elif token == "(":
            if not expect_operand:
                raise ValueError("Missing operator before '('.")
            operators.push(token)
            expect_operand = True

        elif token == ")":
            if expect_operand:
                raise ValueError("Unexpected ')' or missing operand.")
            while not operators.is_empty() and operators.peek() != "(":
                output.append(operators.pop())
            if operators.is_empty():
                raise ValueError("Mismatched parentheses: missing '('.")
            operators.pop()
            expect_operand = False

        elif token in OPERATORS:
            # Support unary + and - by translating them to 0 +/- operand.
            if expect_operand:
                if token in ("+", "-"):
                    output.append("0")
                else:
                    raise ValueError(f"Operator {token!r} has no left operand.")

            precedence = OPERATORS[token][0]
            while (
                not operators.is_empty()
                and operators.peek() in OPERATORS
                and OPERATORS[operators.peek()][0] >= precedence
            ):
                output.append(operators.pop())
            operators.push(token)
            expect_operand = True

        else:
            raise ValueError(f"Unknown token: {token}")

    if expect_operand:
        raise ValueError("Expression ends with an operator or is incomplete.")

    while not operators.is_empty():
        operator = operators.pop()
        if operator in ("(", ")"):
            raise ValueError("Mismatched parentheses.")
        output.append(operator)

    return output


def evaluate_postfix(postfix):
    """Evaluate postfix notation using an operand stack."""
    values = Stack()

    for token in postfix:
        if re.fullmatch(r"\d+(?:\.\d+)?", token):
            number = float(token)
            values.push(number)
        elif token in OPERATORS:
            if values.size() < 2:
                raise ValueError(f"Not enough operands for {token!r}.")
            right = values.pop()
            left = values.pop()

            if token == "+":
                result = left + right
            elif token == "-":
                result = left - right
            elif token == "*":
                result = left * right
            else:
                if right == 0:
                    raise ZeroDivisionError("Division by zero is not allowed.")
                result = left / right
            values.push(result)
        else:
            raise ValueError(f"Invalid postfix token: {token}")

    if values.size() != 1:
        raise ValueError("Expression is malformed.")
    return values.pop()


def evaluate_expression(expression):
    """Evaluate a normal mathematical expression."""
    return evaluate_postfix(to_postfix(tokenize(expression)))


def format_result(value):
    """Avoid unnecessary .0 for whole-number answers."""
    if abs(value - round(value)) < 1e-10:
        return str(int(round(value)))
    return f"{value:.10g}"


def process_files(input_path="input.txt", output_path="output.txt"):
    """Read input expressions and write results, retaining separators."""
    input_file = Path(input_path)
    output_file = Path(output_path)

    if not input_file.exists():
        raise FileNotFoundError(
            f"Input file '{input_file}' was not found. Put it beside this program."
        )

    output_lines = []
    for line_number, raw_line in enumerate(
        input_file.read_text(encoding="utf-8").splitlines(), start=1
    ):
        line = raw_line.strip()

        if not line:
            output_lines.append("")
        elif re.fullmatch(r"-+", line):
            output_lines.append(line)
        else:
            try:
                answer = evaluate_expression(line)
                output_lines.append(format_result(answer))
            except (ValueError, ZeroDivisionError, IndexError) as error:
                output_lines.append(f"ERROR on input line {line_number}: {error}")

    output_file.write_text("\n".join(output_lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    try:
        process_files()
        print("Evaluation complete. Results have been saved to output.txt.")
    except (OSError, FileNotFoundError) as error:
        print(f"File error: {error}")
