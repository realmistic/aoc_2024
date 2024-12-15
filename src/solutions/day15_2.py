from re import L
from src.utils.input_reader import read_lines, read_numbers
import numpy as np

def parse_input(data):
    """Parse input into grid and commands."""
    separator_idx = data.index('')
    grid_lines = data[:separator_idx]
    grid = np.array([list(line) for line in grid_lines])
    commands = []
    for line in data[separator_idx + 1:]:
        commands.extend(list(line))
    return grid, commands

def attempt_move(grid, field, command):
    move = {
        '>':(0, 1),
        'v':(1, 0),
        '<':(0, -1),
        '^':(-1, 0)
    }

    nx = field[0] + move[command][0]
    ny = field[1] + move[command][1]
    
    can_move = -1

    if grid[nx,ny] in ['.']:
        grid[nx,ny] = grid[field]
        grid[field] = '.'
        can_move = 1
    elif grid[nx,ny] == 'O':
        moved = attempt_move(grid,(nx,ny), command)
        if moved > 0:
            grid[nx,ny] = grid[field]
            grid[field] = '.'
            can_move = 1
    
    return can_move

def get_next_position(pos, command):
    """Get next position based on command"""
    move = {
        '>':(0, 1),
        'v':(1, 0),
        '<':(0, -1),
        '^':(-1, 0)
    }
    return (pos[0] + move[command][0], pos[1] + move[command][1])

def is_valid_position(grid, pos):
    """Check if position is within grid bounds"""
    rows, cols = grid.shape
    return 0 <= pos[0] < rows and 0 <= pos[1] < cols

def can_move_to(grid, pos, next_pos):
    """Check if a position is empty"""
    if not is_valid_position(grid, next_pos):
        return False
    return grid[next_pos] == '.'

def find_connected_piece(grid, pos):
    """Find the other part of a connected piece"""
    rows, cols = grid.shape
    x, y = pos
    
    if grid[x,y] == '[' and y + 1 < cols and grid[x,y+1] == ']':
        return (x, y+1)
    elif grid[x,y] == ']' and y - 1 >= 0 and grid[x,y-1] == '[':
        return (x, y-1)
    return None

def attempt_move_part2(grid, command):
    """Non-recursive version that moves all eligible pieces at once"""
    rows, cols = grid.shape
    moves = []  # Store all possible moves
    
    # First pass: find all movable pieces
    for i in range(rows):
        for j in range(cols):
            if grid[i,j] == '[':
                connected = find_connected_piece(grid, (i,j))
                if connected is None:
                    continue
                
                next_pos_left = get_next_position((i,j), command)
                next_pos_right = get_next_position(connected, command)
                
                # Check if both parts can move and won't collide with other pieces
                if (is_valid_position(grid, next_pos_left) and 
                    is_valid_position(grid, next_pos_right) and
                    can_move_to(grid, (i,j), next_pos_left) and 
                    can_move_to(grid, connected, next_pos_right)):
                    
                    # Check if the move would break any other connected pieces
                    valid_move = True
                    for x in range(rows):
                        for y in range(cols):
                            if grid[x,y] in ['[', ']']:
                                other_connected = find_connected_piece(grid, (x,y))
                                if other_connected:
                                    if ((x,y) == next_pos_left or (x,y) == next_pos_right or
                                        other_connected == next_pos_left or other_connected == next_pos_right):
                                        valid_move = False
                                        break
                        if not valid_move:
                            break
                    
                    if valid_move:
                        moves.append(((i,j), connected))
    
    # Second pass: apply all valid moves
    moved = False
    for left_pos, right_pos in moves:
        next_left = get_next_position(left_pos, command)
        next_right = get_next_position(right_pos, command)
        
        # Double check the positions are still empty
        if (can_move_to(grid, left_pos, next_left) and 
            can_move_to(grid, right_pos, next_right)):
            # Move both parts
            grid[next_left] = '['
            grid[next_right] = ']'
            grid[left_pos] = '.'
            grid[right_pos] = '.'
            moved = True
    
    # Move the robot
    robot_pos = np.where(grid == '@')
    if len(robot_pos[0]) > 0:
        x, y = robot_pos[0][0], robot_pos[1][0]
        next_pos = get_next_position((x,y), command)
        if (is_valid_position(grid, next_pos) and 
            can_move_to(grid, (x,y), next_pos)):
            grid[next_pos] = '@'
            grid[x,y] = '.'
            moved = True
    
    return 1 if moved else -1

def calc_grid_value(grid)->int:
    sum = 0
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i,j] in ['O','[']:
                sum+=100*i+j
    return sum

def transform_grid_part2(grid)->np.ndarray:
    rows = len(grid)
    cols = len(grid[0])
    grid_transformed = np.full((rows, 2*cols),'.', dtype='<U1')
    for i in range(rows):
        for j in range(cols):
            if grid[i,j] == '#':
                 grid_transformed[i,2*j] = '#'
                 grid_transformed[i,2*j+1] = '#'
            elif grid[i,j] == 'O':
                 grid_transformed[i,2*j] = '['
                 grid_transformed[i,2*j+1] = ']'
            elif grid[i,j] == '.':
                 grid_transformed[i,2*j] = '.'
                 grid_transformed[i,2*j+1] = '.'
            elif grid[i,j] == '@':
                 grid_transformed[i,2*j] = '@'
                 grid_transformed[i,2*j+1] = '.'
    return grid_transformed

def solve_part1(grid, commands) -> int:
    """Solve part 1 of the puzzle."""
    robot_position = np.where(grid == '@')
    x, y = (robot_position[0][0], robot_position[1][0])

    for command in commands:
        if attempt_move(grid, (x,y), command)>0:
            robot_position = np.where(grid == '@')
            x, y = (robot_position[0][0], robot_position[1][0])

    return calc_grid_value(grid)

def solve_part2(grid, commands) -> int:
    """Solve part 2 of the puzzle."""
    grid2 = transform_grid_part2(grid)

    for command in commands:
        attempt_move_part2(grid2, command)

    return calc_grid_value(grid2)

def main():
    data = read_lines(15)
    grid, commands = parse_input(data)
    
    part1_result = solve_part1(grid, commands)
    print(f"Part 1: {part1_result}")
    
    print('Starting part 2:')
    part2_result = solve_part2(grid, commands)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
