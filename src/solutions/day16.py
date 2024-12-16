from src.utils.input_reader import read_lines
from typing import List, Tuple, Set, Dict
from collections import defaultdict, deque
import sys

# Direction vectors (row, col) for East, South, West, North
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
DIR_CHARS = ['>', 'v', '<', '^']

def parse_maze(data: List[str]) -> Tuple[List[List[str]], Tuple[int, int], Tuple[int, int]]:
    """Parse the maze and return the matrix and start/end positions."""
    matrix = [list(line) for line in data]
    start_pos = None
    end_pos = None
    
    for row_idx, line in enumerate(data):
        for col_idx, char in enumerate(line):
            if char == 'S':
                start_pos = (row_idx, col_idx)
            elif char == 'E':
                end_pos = (row_idx, col_idx)
    
    return matrix, start_pos, end_pos

def is_valid_move(matrix: List[List[str]], pos: Tuple[int, int]) -> bool:
    """Check if position is within bounds and not a wall"""
    rows, cols = len(matrix), len(matrix[0])
    row, col = pos
    return (0 <= row < rows and 
            0 <= col < cols and 
            matrix[row][col] != '#')

def get_next_pos(pos: Tuple[int, int], direction: int) -> Tuple[int, int]:
    """Get next position based on current position and direction"""
    row, col = pos
    drow, dcol = DIRECTIONS[direction]
    return (row + drow, col + dcol)

def find_all_min_score_paths(matrix: List[List[str]], start: Tuple[int, int], 
                           end: Tuple[int, int]) -> Tuple[int, Set[Tuple[int, int]]]:
    """Find all paths with minimum score and return set of tiles used in these paths."""
    # Queue: (score, pos, direction, turns, steps, visited_tiles)
    queue = [(0, start, 0, 0, 0, {start})]
    # visited: (pos, direction) -> (score, turns, steps)
    best_scores = defaultdict(lambda: (float('inf'), float('inf'), float('inf')))
    best_scores[(start, 0)] = (0, 0, 0)
    
    min_score = float('inf')
    all_path_tiles = set()
    
    while queue:
        score, pos, direction, turns, steps, path_tiles = queue.pop(0)
        
        if score > min_score:
            continue
            
        if pos == end:
            if score <= min_score:
                if score < min_score:
                    min_score = score
                    all_path_tiles = path_tiles.copy()
                else:
                    all_path_tiles.update(path_tiles)
                continue
        
        # Try moving forward
        next_pos = get_next_pos(pos, direction)
        if is_valid_move(matrix, next_pos):
            new_score = score + 1
            new_state = (next_pos, direction)
            curr_best = best_scores[new_state]
            
            if new_score <= curr_best[0]:
                new_tiles = path_tiles | {next_pos}
                queue.append((new_score, next_pos, direction, turns, steps + 1, new_tiles))
                best_scores[new_state] = (new_score, turns, steps + 1)
        
        # Try turning left or right
        for turn in [-1, 1]:
            new_direction = (direction + turn) % 4
            next_pos = get_next_pos(pos, new_direction)
            if is_valid_move(matrix, next_pos):
                new_score = score + 1001  # 1000 for turn + 1 for step
                new_state = (next_pos, new_direction)
                curr_best = best_scores[new_state]
                
                if new_score <= curr_best[0]:
                    new_tiles = path_tiles | {next_pos}
                    queue.append((new_score, next_pos, new_direction, turns + 1, steps + 1, new_tiles))
                    best_scores[new_state] = (new_score, turns + 1, steps + 1)
    
    return min_score, all_path_tiles

def visualize_best_paths(data: List[str], best_tiles: Set[Tuple[int, int]]) -> None:
    """Visualize all tiles that are part of any best path with 'O'"""
    maze = [list(row) for row in data]
    for row, col in best_tiles:
        if maze[row][col] not in ['S', 'E']:
            maze[row][col] = 'O'
    
    print("\nBest paths visualization (O = part of a best path):")
    for row in maze:
        print(''.join(row))

def solve_part1(data: List[str]) -> int:
    """Solve part 1: Find minimum score path through maze"""
    matrix, start_pos, end_pos = parse_maze(data)
    min_score, _ = find_all_min_score_paths(matrix, start_pos, end_pos)
    return min_score

def solve_part2(data: List[str]) -> int:
    """Solve part 2: Count tiles that are part of any best path"""
    matrix, start_pos, end_pos = parse_maze(data)
    _, best_tiles = find_all_min_score_paths(matrix, start_pos, end_pos)
    visualize_best_paths(data, best_tiles)
    return len(best_tiles)

def main():
    data = read_lines(16)
    
    part1_result = solve_part1(data)
    print(f"Part 1: {part1_result}")
    
    part2_result = solve_part2(data)
    print(f"\nPart 2: {part2_result}")

if __name__ == "__main__":
    main()
