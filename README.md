DTECH320 - Stack-Based Expression Evaluator

 Files
- main.py — Python implementation of a Stack class and expression evaluator.
- input.txt — sample expressions, separated by lines of hyphens.
- output.txt — generated results from the sample input.
- Student_Report.docx — report describing the data structure, design, testing, and results.

Requirements
- Python 3.8 or newer
- No external Python packages are required.

 How to run
1. Place main.py and input.txt in the same folder.
2. Open a terminal or command prompt in that folder.
3. Run python main.py.
4. Read the generated output.txt.

 Input format
Put one mathematical expression on each line. A line containing only hyphens (for example -----) is a separator. Supported operators are +, -, *, /, parentheses, and decimal numbers. Multiplication and division have higher precedence than addition and subtraction.

 Assumptions and limitations
- Expressions use ordinary infix notation.
- Exponentiation is not supported because it is not listed in the assignment.
- Division by zero and malformed expressions produce an error message in output.txt.
- Blank lines are preserved.
