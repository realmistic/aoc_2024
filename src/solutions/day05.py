from src.utils.input_reader import read_lines, read_numbers
from typing import List, Tuple, Dict

def parse_input(data: List[str]) -> Tuple[List[Tuple[str, str]], List[List[str]], Dict[int, str]]:
    """
    Parse the input into:
    1. List of string pairs before empty line
    2. List of lists of values (not dictionaries anymore as we need to modify them)
    3. Dictionary mapping list index to its middle value
    """
    first_part = []
    second_part = []
    middle_values = {}
    
    # Find the empty line that separates the two parts
    empty_line_idx = data.index('')
    
    # Parse first part - pairs of strings
    for line in data[:empty_line_idx]:
        left, right = line.split('|')
        first_part.append((left.strip(), right.strip()))
    
    # Parse second part - keep as lists to allow modification
    for list_idx, line in enumerate(data[empty_line_idx + 1:]):
        if line:  # Skip any additional empty lines
            values = [num.strip() for num in line.split(',')]
            second_part.append(values)
            
            # Find and store middle value
            middle_idx = len(values) // 2
            middle_values[list_idx] = values[middle_idx]
    
    return first_part, second_part, middle_values

def get_position_dict(values: List[str]) -> Dict[str, int]:
    """Convert list of values to position dictionary"""
    return {value: idx for idx, value in enumerate(values)}

def is_valid_list(pairs: List[Tuple[str, str]], values: List[str]) -> bool:
    """
    Check if a list is valid based on pair positions.
    """
    position_dict = get_position_dict(values)
    for left, right in pairs:
        if left in position_dict and right in position_dict:
            if position_dict[left] >= position_dict[right]:
                return False
    return True

def fix_list_ordering(pairs: List[Tuple[str, str]], values: List[str]) -> List[str]:
    """
    Fix the ordering of values in a list by swapping values that violate pair rules.
    Returns a new list with corrected ordering.
    """
    fixed_values = values.copy()
    position_dict = get_position_dict(fixed_values)
    
    print(f"\nFixing list: {','.join(values)}")
    
    # Keep swapping until all pairs are in correct order
    changes_made = True
    while changes_made:
        changes_made = False
        for left, right in pairs:
            if left in position_dict and right in position_dict:
                left_pos = position_dict[left]
                right_pos = position_dict[right]
                if left_pos >= right_pos:
                    # Swap the values
                    fixed_values[left_pos], fixed_values[right_pos] = fixed_values[right_pos], fixed_values[left_pos]
                    # Update position dictionary
                    position_dict = get_position_dict(fixed_values)
                    changes_made = True
                    print(f"Swapped {left}({left_pos}) with {right}({right_pos})")
                    print(f"New order: {','.join(fixed_values)}")
    
    print(f"Final order: {','.join(fixed_values)}")
    print(f"Middle value: {get_middle_value(fixed_values)}")
    return fixed_values

def get_middle_value(values: List[str]) -> str:
    """Get middle value from a list"""
    middle_idx = len(values) // 2
    return values[middle_idx]

def solve_part1(data) -> int:
    """
    Solve part 1 of the puzzle.
    Sum of middle values from valid lists.
    """
    pairs, lists, _ = parse_input(data)
    valid_lists = [lst for lst in lists if is_valid_list(pairs, lst)]
    return sum(int(get_middle_value(lst)) for lst in valid_lists)

def solve_part2(data) -> int:
    """
    Solve part 2 of the puzzle.
    Sum of middle values from fixed invalid lists.
    """
    pairs, lists, _ = parse_input(data)
    
    # Get only invalid lists
    invalid_lists = [lst for lst in lists if not is_valid_list(pairs, lst)]
    print(f"\nFound {len(invalid_lists)} invalid lists")
    
    # Fix each invalid list and get its new middle value
    fixed_middle_values = []
    for i, lst in enumerate(invalid_lists):
        print(f"\nProcessing invalid list {i+1}/{len(invalid_lists)}")
        fixed_list = fix_list_ordering(pairs, lst)
        middle_value = get_middle_value(fixed_list)
        fixed_middle_values.append(int(middle_value))
    
    total = sum(fixed_middle_values)
    print(f"\nTotal sum of middle values from fixed lists: {total}")
    return total

def main():
    # Read the input
    data = read_lines(5)
    
    # Solve part 1
    part1_result = solve_part1(data)
    print(f"Part 1: {part1_result}")
    
    # Solve part 2
    part2_result = solve_part2(data)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
