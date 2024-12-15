from re import L
from src.utils.input_reader import read_lines, read_numbers
import numpy as np
from collections import defaultdict, deque
from tqdm import tqdm

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

def get_connected_piece(grid, pos):
    """Get the connected piece position"""
    x, y = pos
    if grid[x,y] == '[' and y + 1 < grid.shape[1] and grid[x,y+1] == ']':
        return (x, y+1)
    elif grid[x,y] == ']' and y - 1 >= 0 and grid[x,y-1] == '[':
        return (x, y-1)
    return None

def get_boxes_in_direction(grid, start_pos, command):
    """Get boxes in the direction of movement"""
    move = {
        '>':(0, 1),
        'v':(1, 0),
        '<':(0, -1),
        '^':(-1, 0)
    }
    dx, dy = move[command]
    x, y = start_pos
    boxes = []
    
    while True:
        x += dx
        y += dy
        if not is_valid_position(grid, (x, y)):
            break
        if grid[x, y] in ['[', ']']:
            boxes.append((x, y))
    return boxes

def find_boxes_to_move(grid, command):
    """Find all boxes that need to be moved in this push, in order from first to last"""
    rows, cols = grid.shape
    boxes_to_move = []  # Will store (left_pos, right_pos) tuples
    processed = set()
    
    # Determine scan direction based on command
    if command == '^':
        scan_rows = range(rows)
    elif command == 'v':
        scan_rows = range(rows-1, -1, -1)
    elif command == '<':
        scan_cols = range(cols)
    else:  # command == '>'
        scan_cols = range(cols-1, -1, -1)
    
    # Scan grid in appropriate direction
    if command in ['^', 'v']:
        for i in scan_rows:
            for j in range(cols):
                if grid[i,j] == '[' and (i,j) not in processed:
                    # Only check boxes in movement direction
                    boxes = get_boxes_in_direction(grid, (i,j), command)
                    for box_pos in boxes:
                        if box_pos in processed:
                            continue
                        
                        other = get_connected_piece(grid, box_pos)
                        if other is None or other in processed:
                            continue
                            
                        next_pos = get_next_position(box_pos, command)
                        next_other = get_next_position(other, command)
                        
                        if not (is_valid_position(grid, next_pos) and is_valid_position(grid, next_other)):
                            continue
                            
                        if grid[next_pos] == '.' and grid[next_other] == '.':
                            left = box_pos if grid[box_pos] == '[' else other
                            right = other if grid[box_pos] == '[' else box_pos
                            boxes_to_move.append((left, right))
                            processed.add(box_pos)
                            processed.add(other)
    else:
        for j in scan_cols:
            for i in range(rows):
                if grid[i,j] == '[' and (i,j) not in processed:
                    # Only check boxes in movement direction
                    boxes = get_boxes_in_direction(grid, (i,j), command)
                    for box_pos in boxes:
                        if box_pos in processed:
                            continue
                        
                        other = get_connected_piece(grid, box_pos)
                        if other is None or other in processed:
                            continue
                            
                        next_pos = get_next_position(box_pos, command)
                        next_other = get_next_position(other, command)
                        
                        if not (is_valid_position(grid, next_pos) and is_valid_position(grid, next_other)):
                            continue
                            
                        if grid[next_pos] == '.' and grid[next_other] == '.':
                            left = box_pos if grid[box_pos] == '[' else other
                            right = other if grid[box_pos] == '[' else box_pos
                            boxes_to_move.append((left, right))
                            processed.add(box_pos)
                            processed.add(other)
    
    return boxes_to_move

def attempt_move_part2(grid, command):
    """Move all boxes in the correct order"""
    moved = False
    
    while True:
        any_moved = False
        
        # Find all boxes that need to be moved
        boxes_to_move = find_boxes_to_move(grid, command)
        if not boxes_to_move:
            break
            
        # Move boxes in reverse order (last to first)
        for left, right in reversed(boxes_to_move):
            next_left = get_next_position(left, command)
            next_right = get_next_position(right, command)
            
            # Move the box
            grid[next_left] = '['
            grid[next_right] = ']'
            grid[left] = '.'
            grid[right] = '.'
            any_moved = True
            moved = True
        
        # Move robot after boxes have moved
        robot_pos = np.where(grid == '@')
        if len(robot_pos[0]) > 0:
            x, y = robot_pos[0][0], robot_pos[1][0]
            next_pos = get_next_position((x,y), command)
            if (is_valid_position(grid, next_pos) and grid[next_pos] == '.'):
                grid[next_pos] = '@'
                grid[x,y] = '.'
                any_moved = True
                moved = True
        
        if not any_moved:
            break
    
    return 1 if moved else -1

def calc_grid_value(grid)->int:
    """Calculate grid value based on the actual positions in the grid"""
    sum = 0
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            if grid[i,j] == 'O' or grid[i,j] == '[':
                sum += 100*i + j
    return sum

def transform_grid_part2(grid)->np.ndarray:
    """Transform grid for part 2, doubling the width"""
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

    print(f"Processing {len(commands)} commands...")
    for command in tqdm(commands, desc="Processing commands"):
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
