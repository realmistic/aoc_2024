from src.utils.input_reader import read_lines
from itertools import product

def concatenate_numbers(a, b):
    """
    Concatenate two numbers.
    
    Args:
        a: First number
        b: Second number
    
    Returns:
        Concatenated number (e.g., 12, 345 -> 12345)
    """
    return int(str(a) + str(b))

def evaluate_expression(numbers, operators):
    """
    Evaluate expression left-to-right with given numbers and operators.
    
    Args:
        numbers: List of integers
        operators: List of operators ('+', '*', or '||')
    
    Returns:
        Result of the expression
    """
    if not operators:  # Single number case
        return numbers[0]
        
    result = numbers[0]
    for i, op in enumerate(operators):
        if op == '+':
            result += numbers[i + 1]
        elif op == '*':
            result *= numbers[i + 1]
        else:  # op == '||'
            result = concatenate_numbers(result, numbers[i + 1])
    return result

def can_match_test_value(test_value, numbers, include_concat=False):
    """
    Check if it's possible to match test value using combinations of operators.
    
    Args:
        test_value: Target value to match
        numbers: List of numbers to combine with operators
        include_concat: Whether to include concatenation operator
    
    Returns:
        True if test value can be matched, False otherwise
    """
    if len(numbers) == 1:
        return numbers[0] == test_value
        
    # Define possible operators based on part
    possible_operators = ['+', '*']
    if include_concat:
        possible_operators.append('||')
    
    # Generate all possible combinations of operators
    all_operator_combinations = product(possible_operators, repeat=len(numbers)-1)
    
    # Try each combination of operators
    for operators in all_operator_combinations:
        try:
            if evaluate_expression(numbers, operators) == test_value:
                return True
        except:
            continue
    
    return False

def parse_line(line):
    """
    Parse input line into test value and numbers.
    
    Args:
        line: Input line in format "test_value: num1 num2 ..."
    
    Returns:
        Tuple of (test_value, list of numbers)
    """
    test_part, nums_part = line.split(':')
    test_value = int(test_part)
    numbers = [int(x) for x in nums_part.split()]
    return test_value, numbers

def solve_part1(data) -> int:
    """
    Solve part 1 of the puzzle.
    
    Args:
        data: List of input lines
    
    Returns:
        Sum of test values from valid equations using only + and *
    """
    total = 0
    
    for line in data:
        test_value, numbers = parse_line(line)
        if can_match_test_value(test_value, numbers, include_concat=False):
            total += test_value
    
    return total

def solve_part2(data) -> int:
    """
    Solve part 2 of the puzzle.
    
    Args:
        data: List of input lines
    
    Returns:
        Sum of test values from valid equations using +, *, and ||
    """
    total = 0
    
    for line in data:
        test_value, numbers = parse_line(line)
        if can_match_test_value(test_value, numbers, include_concat=True):
            total += test_value
    
    return total

def main():
    # Read the input
    data = read_lines(7)
    
    # Solve part 1
    part1_result = solve_part1(data)
    print(f"Part 1: {part1_result}")
    
    # Solve part 2
    part2_result = solve_part2(data)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
