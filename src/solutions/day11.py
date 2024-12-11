from src.utils.input_reader import read_lines, read_numbers
from collections import defaultdict

def solve_with_blinks_showing_evolution(data: list, num_blinks: int) -> int:
    """
    Original solution that shows full array evolution.
    Used for part 1 where we want to see the process.
    """
    input = [x for x in data[0].split(' ')]
    current = input
    
    print('Initial arrangement:')
    print(current,'\n')
    
    for i in range(num_blinks):
        new_state = []
        for elem in current:
            l,r = blink(elem)
            if r is None:
                new_state.append(l)
            else:
                new_state.append(l)
                new_state.append(r)
        print(f'After {i+1} blinks:')
        print(new_state,'\n')
        print(f'Result is count stones = {len(new_state)}')
        current = new_state
    
    return len(current)

def solve_with_blinks_optimized(data: list, num_blinks: int) -> int:
    """
    Optimized solution that only tracks counts.
    Used for part 2 where performance matters.
    """
    number_counts = defaultdict(int)
    for num in data[0].split(' '):
        number_counts[num] += 1
    
    print("\nBlink progression:")
    print(f"Initial state - Unique numbers: {len(number_counts)}, Total numbers: {sum(number_counts.values())}, Average count: {sum(number_counts.values())/len(number_counts):.2f}")
    
    for i in range(num_blinks):
        new_counts = defaultdict(int)
        for num, count in number_counts.items():
            l, r = blink(num)
            if r is None:
                new_counts[l] += count
            else:
                new_counts[l] += count
                new_counts[r] += count
        number_counts = new_counts
        avg_count = sum(number_counts.values())/len(number_counts)
        print(f"Blink {i+1} - Unique numbers: {len(number_counts)}, Total numbers: {sum(number_counts.values())}, Average count: {avg_count:.2f}")
    
    return sum(number_counts.values())

def solve_part1(data) -> int:
    """
    Solve part 1 of the puzzle.
    Shows full evolution of the array.
    """
    return solve_with_blinks_showing_evolution(data, 25)

def solve_part2(data) -> int:
    """
    Solve part 2 of the puzzle.
    Uses optimized solution for performance.
    """
    return solve_with_blinks_optimized(data, 75)

def blink(num:str) -> str:
    if num == '0':
        return '1', None
    elif len(num)%2==0:
        left = num[:len(num)//2]
        right =str(int(num[len(num)//2:])) #remove leading zeros
        return left, right
    else:
        return str(2024*int(num)), None    

def main():
    # Read the input
    data = read_lines(11)
    
    # Solve part 1
    part1_result = solve_part1(data)
    print(f"Part 1: {part1_result}")
    
    # Solve part 2
    part2_result = solve_part2(data)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
