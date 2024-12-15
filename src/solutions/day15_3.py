from itertools import product
from src.utils.input_reader import read_lines

EMPTY = '.'
WALL = '#'
BOX = 'O'
ROBOT = '@'
BIG_BOX_LEFT = '['
BIG_BOX_RIGHT = ']'

EXPANDED_EMPTY = [EMPTY, EMPTY]
EXPANDED_WALL = [WALL, WALL]
EXPANDED_BOX = [BIG_BOX_LEFT, BIG_BOX_RIGHT]
EXPANDED_ROBOT = [ROBOT, EMPTY]

EXPANSIONS = {
    EMPTY: EXPANDED_EMPTY,
    WALL: EXPANDED_WALL,
    BOX: EXPANDED_BOX,
    ROBOT: EXPANDED_ROBOT
}

def parse_input(data):
    """Parse input into grid and commands"""
    separator_idx = data.index('')
    grid = [list(line) for line in data[:separator_idx]]
    instructions = ''.join(data[separator_idx + 1:])
    
    expanded_grid = [
        [symbol for expanded_value in row for symbol in EXPANSIONS.get(expanded_value, [expanded_value])]
        for row in grid
    ]
    
    return grid, expanded_grid, instructions

def get_start_pos(grid):
    rows, cols = len(grid), len(grid[0])
    for x, y in product(range(rows), range(cols)):
        if grid[x][y] == ROBOT:
            return (x, y)

def convert_symbols_to_directions(symbols):
    direction_map = {
        '<': (0, -1),  # Left
        '>': (0, 1),   # Right
        '^': (-1, 0),  # Up
        'v': (1, 0)    # Down
    }
    return [direction_map[symbol] for symbol in symbols]

def move_object(start_pos, dir, grid):
    x, y = start_pos[0], start_pos[1]
    targetx, targety = x + dir[0], y + dir[1]
    obj = grid[x][y]
    
    if grid[targetx][targety] == WALL:
        return False
    elif grid[targetx][targety] == EMPTY:
        pass
    elif not move_object((targetx, targety), dir, grid):
        return False
    
    grid[targetx][targety] = obj
    grid[x][y] = EMPTY
    return True

def move_object_on_expanded_grid(start_pos, dir, grid, swap=True, check=True):
    """Move object in expanded grid, handling box pairs appropriately.
    
    Args:
        start_pos: Starting position (x, y) of the object to move
        dir: Direction to move (dx, dy)
        grid: The game grid
        swap: Controls whether to actually perform the move or just check if it's possible
              When True: Updates the grid by moving objects to their new positions
              When False: Only checks if the move would be valid without modifying the grid
              This is used to verify moves are possible before committing to them
        check: Controls whether to verify if connected box parts can move
               When True: Recursively checks if both parts of a box can move
               When False: Assumes the move is possible without checking connected parts
               This prevents infinite recursion when moving connected box parts
               
    For example, when moving a box vertically:
    1. First check if both parts can move (swap=False) to validate the move
    2. If both checks pass, move the matching part (swap=True, check=False)
    3. Finally move the current part
    
    The check parameter prevents infinite recursion by stopping the recursive checking
    of connected parts, while swap controls whether we're just checking or actually moving.
    """
    x, y = start_pos[0], start_pos[1]
    targetx, targety = x + dir[0], y + dir[1]
    obj = grid[x][y]
    
    if grid[targetx][targety] == WALL:
        return False
    elif grid[targetx][targety] == EMPTY:
        if swap:
            grid[targetx][targety] = obj
            grid[x][y] = EMPTY
        return True
    elif grid[targetx][targety] in (BIG_BOX_LEFT, BIG_BOX_RIGHT):
        if grid[targetx][targety] == BIG_BOX_LEFT:
            matching_x, matching_y = targetx, targety + 1
        else:
            matching_x, matching_y = targetx, targety - 1
            
        if dir in ((1, 0), (-1, 0)):
            if check and not move_object_on_expanded_grid((matching_x, matching_y), dir, grid, swap=False):
                return False
            if check and not move_object_on_expanded_grid((targetx, targety), dir, grid, swap=False):
                return False
            if swap:
                move_object_on_expanded_grid((matching_x, matching_y), dir, grid, swap=True, check=False)
        
        if swap:
            moved = move_object_on_expanded_grid((targetx, targety), dir, grid)
            if moved:
                grid[targetx][targety] = obj
                grid[x][y] = EMPTY
                return True
            else:
                return False
                
        return True
    
    return False

def compute_score(grid, part2=False):
    rows, cols = len(grid), len(grid[0])
    check = BOX
    if part2:
        check = BIG_BOX_LEFT
    return sum(x * 100 + y for x, y in product(range(rows), range(cols)) if grid[x][y] == check)

def main():
    data = read_lines(15)
    grid, expanded_grid, instructions = parse_input(data)
    
    # Part 1
    robot_pos = get_start_pos(grid)
    dirs = convert_symbols_to_directions(instructions)
    
    for dir in dirs:
        if move_object(robot_pos, dir, grid):
            robot_pos = (robot_pos[0] + dir[0], robot_pos[1] + dir[1])
    
    print('Part 1:', compute_score(grid))
    
    # Part 2
    robot_pos = get_start_pos(expanded_grid)
    
    for dir in dirs:
        if move_object_on_expanded_grid(robot_pos, dir, expanded_grid):
            robot_pos = (robot_pos[0] + dir[0], robot_pos[1] + dir[1])
    
    print('Part 2:', compute_score(expanded_grid, True))

if __name__ == "__main__":
    main()
