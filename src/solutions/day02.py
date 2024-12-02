import numpy as np
from src.utils.input_reader import read_numbers

def check_safe(arr: list[int]) -> bool:
    differences = [np.abs(arr[i] - arr[i + 1]) for i in range(len(arr) - 1)]
    is_sorted = arr == sorted(arr)
    is_sorted_desc = arr == sorted(arr, reverse=True)
    min_diff = np.min(differences)
    max_diff = np.max(differences)
    
    return (is_sorted or is_sorted_desc) and min_diff >= 1 and max_diff <= 3

def check_reduced(arr: list[int], num: int) -> bool:
    arr_reduced = [arr[j] for j in range(len(arr)) if j != num]
    return check_safe(arr_reduced)

def solve_part1(numbers: list[list[int]]) -> int:
    return sum(1 for arr in numbers if check_safe(arr))

def solve_part2(numbers: list[list[int]]) -> int:
    count = 0
    for arr in numbers:
        for i in range(len(arr)):
            if check_reduced(arr, i):
                count += 1
                break
    return count

def main():
    numbers = read_numbers(2)
    
    part1_result = solve_part1(numbers)
    print(f"Part 1: {part1_result}")
    
    part2_result = solve_part2(numbers)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
