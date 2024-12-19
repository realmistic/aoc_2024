from src.utils.input_reader import read_lines

def solve_part1(data) -> int:
    """
    Solve part 1 of the puzzle.
    
    Args:
        data: Puzzle input

    Returns:
        Solution to part 1
    """
    # First line contains patterns
    patterns = [pattern.strip() for pattern in data[0].split(',')]
    
    # Skip empty line and get designs
    designs = [line.strip() for line in data[2:] if line.strip()]
    
    print(patterns)
    print(designs)

    count =0
    for design in designs:
        available = is_available(design=design,patterns=patterns)
        if available:
            count+=1
        print(f'Checking design  ={design}, available = {available}, current count of available designs={count}')

    return count

def is_available(design:str, patterns):
    if len(design)==0:
        return True
    for p in patterns:
        if design.startswith(p):
            remainder = design[len(p):]
            # DEBUG: print(design, p, remainder)
            if is_available(remainder, patterns=patterns):
                return True
    return False

def count_available(design:str, patterns:list[str], memo:dict=None) -> int:
    if memo is None:
        memo = {}
    
    if design in memo:
        return memo[design]
    
    if len(design) == 0:
        return 1
        
    total = 0
    for p in patterns:
        if design.startswith(p):
            remainder = design[len(p):]
            total += count_available(remainder, patterns, memo)
    
    memo[design] = total
    return total

def solve_part2(data) -> int:
    """
    Solve part 2 of the puzzle.
    
    Args:
        data: Puzzle input

    Returns:
        Solution to part 2
    """
    # First line contains patterns
    patterns = [pattern.strip() for pattern in data[0].split(',')]
    
    # Skip empty line and get designs
    designs = [line.strip() for line in data[2:] if line.strip()]
    
    total = 0
    for design in designs:
        combinations = count_available(design, patterns)
        print(f"Design {design}: {combinations} combinations")
        total += combinations
    
    return total

def main():
    data = read_lines(19)
    
    part1_result = solve_part1(data)
    print(f"Part 1: {part1_result}")
    
    part2_result = solve_part2(data)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
