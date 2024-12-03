from src.utils.input_reader import read_chars
import re

def solve_part1(data) -> int:
    """
    Solve part 1 of the puzzle.
    
    Args:
        data: Puzzle input

    Returns:
        Solution to part 1
    """
    # Regular expression to match mul(X,Y) where X and Y are 1-3 digit numbers
    pattern = r"mul\((\d{1,3}),(\d{1,3})\)"

    # Find all matches
    matches = re.findall(pattern, data)

    #DEBUG: print(matches)

    rez = 0
    for elem in matches:
        a,b = float(elem[0]), float(elem[1])
        rez += a*b
    return int(rez)

def solve_part2(data) -> int:
    """
    Solve part 2 of the puzzle.
    
    Args:
        data: Puzzle input

    Returns:
        Solution to part 2
    """
    # Pattern to match either prefixes or mul(X,Y)
    pattern = r"(do\(\)|don't\(\))|mul\((\d{1,3}),(\d{1,3})\)"

    # Find all matches
    matches = re.findall(pattern, data)

    # Track the last seen prefix
    last_prefix = "nothing (beginning)"
    results = []

    for match in matches:
        if match[0]:  # If this is a prefix (do() or don't())
            last_prefix = match[0]
        else:  # If this is a mul(X,Y)
            x, y = match[1], match[2]
            results.append({"group_type": last_prefix, "mul": f"mul({x},{y})"})
    
    # print(results)

    rez = 0
    for elem in results:
        if elem['group_type'] != "don't()":
            # print(elem['mul'])
            rez += solve_part1(elem['mul'])

    return rez

def main():
    # Read the input
    data = read_chars(3)  # Using read_lines by default, change if needed
    
    combined_data = ''.join(data)
    # data = data[0] #only one string

    # Test string
    # test_string = "xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"

    # Solve part 1
    part1_result = solve_part1(combined_data)
    print(f"Part 1: {part1_result}")

    # test_data = "xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))"    
    # Solve part 2
    part2_result = solve_part2(combined_data)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
