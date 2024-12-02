import numpy as np
from src.utils.input_reader import read_numbers

def solve_part1(numbers: list[list[int]]) -> int:
    first_numbers = [pair[0] for pair in numbers]
    second_numbers = [pair[1] for pair in numbers]
    
    # Sort both lists
    first_numbers.sort()
    second_numbers.sort()

    # Create arrays and calculate difference
    a = np.array(first_numbers, dtype=np.int64)
    b = np.array(second_numbers, dtype=np.int64)
    c = np.abs(a - b)
    
    return np.sum(c, dtype=np.int64)

def solve_part2(numbers: list[list[int]]) -> int:
    first_numbers = [pair[0] for pair in numbers]
    second_numbers = [pair[1] for pair in numbers]
    
    # Count occurrences of second numbers
    occurencies = {}
    for num in second_numbers:
        occurencies[num] = occurencies.get(num, 0) + 1
    
    # Calculate result
    result = 0
    for elem in first_numbers:
        if elem in occurencies:
            result += elem * occurencies[elem]
    
    return result

def main():
    numbers = read_numbers(1)
    
    part1_result = solve_part1(numbers)
    print(f"Part 1: {part1_result}")
    
    part2_result = solve_part2(numbers)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
