from copy import deepcopy
from src.utils.input_reader import read_lines
import numpy as np
from numpy.typing import NDArray
from typing import Set, Tuple, List
import multiprocessing as mp
import time

# Direction vectors for UP, RIGHT, DOWN, LEFT (in clockwise order)
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

def solve_part1(matrix: NDArray, test_pos: Tuple[int, int] = None) -> int:
    """
    Solve part 1 of the puzzle.
    Track the guard's movement according to the rules:
    1. If there's an obstacle in front, turn right 90 degrees
    2. Otherwise, move forward one step
    
    Args:
        matrix: Numpy array representing the lab map
        test_pos: Optional position to treat as an obstacle for part 2
    
    Returns:
        Number of distinct positions visited by the guard,
        or -1 if a loop is detected
    """
    # Find starting position and initialize direction (0 = UP)
    start_y, start_x = np.where(matrix == '^')
    current_pos = (int(start_y[0]), int(start_x[0]))
    current_dir = 0  # Start facing UP
    
    # Track visited positions
    visited = {current_pos}
    # Track state (position, direction) to detect loops
    states = {(current_pos, current_dir)}
    rows, cols = matrix.shape
    
    while True:
        # Calculate position in front of guard
        dy, dx = DIRECTIONS[current_dir]
        front_pos = (current_pos[0] + dy, current_pos[1] + dx)
        
        # Check if front position is out of bounds, has obstacle, or is test position
        if (not (0 <= front_pos[0] < rows and 0 <= front_pos[1] < cols) or 
            matrix[front_pos] == '#' or front_pos == test_pos):
            # Turn right (clockwise)
            current_dir = (current_dir + 1) % 4
            # Check if we've seen this state before (loop detection)
            if (current_pos, current_dir) in states:
                return -1  # Loop detected
            states.add((current_pos, current_dir))
        else:
            # Move forward
            current_pos = front_pos
            visited.add(current_pos)
            # Check if we've seen this state before (loop detection)
            if (current_pos, current_dir) in states:
                return -1  # Loop detected
            states.add((current_pos, current_dir))
            
            # Check if guard has left the mapped area
            if (current_pos[0] == 0 or current_pos[0] == rows-1 or 
                current_pos[1] == 0 or current_pos[1] == cols-1):
                # One more step would take us out of bounds
                next_pos = (current_pos[0] + DIRECTIONS[current_dir][0], 
                          current_pos[1] + DIRECTIONS[current_dir][1])
                if not (0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols):
                    break
    
    return len(visited)

def solve_part2(matrix: NDArray) -> int:
    """Original part 2 solution"""
    start_time = time.time()
    rows, cols = matrix.shape
    loops = []

    for i in range(rows):
        for j in range(cols):
            if matrix[i,j] == '.':
                matrix[i,j] = '#'
                if solve_part1(matrix) < 0:
                    loops.append((i,j))
                matrix[i,j] = '.'
    
    duration = time.time() - start_time
    print(f"Part 2 original took {duration:.2f} seconds")
    return len(loops)

def get_original_path(matrix: NDArray) -> Set[Tuple[int, int]]:
    """Get the path the guard takes without any additional obstacles"""
    start_y, start_x = np.where(matrix == '^')
    current_pos = (int(start_y[0]), int(start_x[0]))
    current_dir = 0
    path = {current_pos}
    rows, cols = matrix.shape
    
    while True:
        dy, dx = DIRECTIONS[current_dir]
        front_pos = (current_pos[0] + dy, current_pos[1] + dx)
        
        if (not (0 <= front_pos[0] < rows and 0 <= front_pos[1] < cols) or 
            matrix[front_pos] == '#'):
            current_dir = (current_dir + 1) % 4
        else:
            current_pos = front_pos
            path.add(current_pos)
            
            if (current_pos[0] == 0 or current_pos[0] == rows-1 or 
                current_pos[1] == 0 or current_pos[1] == cols-1):
                next_pos = (current_pos[0] + DIRECTIONS[current_dir][0], 
                          current_pos[1] + DIRECTIONS[current_dir][1])
                if not (0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols):
                    break
    
    return path

def check_positions(args) -> List[Tuple[int, int]]:
    """Process a chunk of positions to check for loops"""
    matrix, positions = args
    loops = []
    for pos in positions:
        if solve_part1(matrix, pos) < 0:
            loops.append(pos)
    return loops

def solve_part2_advanced(matrix: NDArray) -> int:
    """
    Optimized part 2 solution using:
    1. Pre-calculate original path
    2. Only test positions near the path
    3. Parallel processing
    4. Avoid matrix modifications
    """
    start_time = time.time()
    
    # Get the original path
    original_path = get_original_path(matrix)
    
    # Get all empty positions near the path
    rows, cols = matrix.shape
    test_positions = []
    for i in range(rows):
        for j in range(cols):
            if matrix[i,j] == '.':
                # Check if position is near the path (within 2 steps)
                for dy in range(-2, 3):
                    for dx in range(-2, 3):
                        if (i+dy, j+dx) in original_path:
                            test_positions.append((i,j))
                            break
                    if (i,j) in test_positions:
                        break
    
    # Split positions into chunks for parallel processing
    num_processes = mp.cpu_count()
    chunk_size = max(1, len(test_positions) // num_processes)
    chunks = [test_positions[i:i + chunk_size] 
             for i in range(0, len(test_positions), chunk_size)]
    
    # Prepare arguments for parallel processing
    args = [(matrix, chunk) for chunk in chunks]
    
    # Process chunks in parallel
    with mp.Pool(processes=num_processes) as pool:
        results = pool.map(check_positions, args)
    
    # Combine results
    loops = []
    for result in results:
        loops.extend(result)
    
    duration = time.time() - start_time
    print(f"Part 2 advanced took {duration:.2f} seconds")
    return len(loops)

def main():
    # Read the input lines and convert to numpy matrix
    data = read_lines(6)
    matrix = np.array([list(line) for line in data])
    
    # Solve part 1
    part1_result = solve_part1(matrix)
    print(f"Part 1: {part1_result}")
    
    # Solve part 2 with both methods
    part2_result = solve_part2(matrix.copy())
    part2_advanced_result = solve_part2_advanced(matrix.copy())
    print(f"Part 2 results - Original: {part2_result}, Advanced: {part2_advanced_result}")

if __name__ == "__main__":
    main()
