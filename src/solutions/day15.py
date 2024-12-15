from re import L
from src.utils.input_reader import read_lines, read_numbers
import numpy as np

def parse_input(data):
    """
    Parse input into grid and commands.
    
    Args:
        data: List of input lines
    
    Returns:
        tuple: (numpy array of grid, list of commands)
    """
    # Find the empty line that separates grid and commands
    separator_idx = data.index('')
    
    # Parse grid into numpy array
    grid_lines = data[:separator_idx]
    grid = np.array([list(line) for line in grid_lines])
    
    # Parse commands into list - join all remaining lines
    commands = []
    for line in data[separator_idx + 1:]:  # Take all lines after separator
        commands.extend(list(line))  # Add each character from each line
    
    # print(grid)
    # print(commands)

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
    
    can_move = -1  # default to can't move

    # print(f'Next position = ({nx, ny})')
    if grid[nx,ny] in ['.']:  # can move to empty space or current position
        grid[nx,ny] = grid[field]
        grid[field] = '.'  # clear original position
        can_move = 1
    elif grid[nx,ny] == 'O':  # try to move that field first
        moved = attempt_move(grid,(nx,ny), command)
        if moved > 0:  # next moved --> can move now
            grid[nx,ny] = grid[field]
            grid[field] = '.'  # clear original position
            can_move = 1
    # else: it's a wall or something else, keep can_move as -1
    
    return can_move

# need to be able for simult move
def can_be_moved(grid, field, command):
    move = {
        '>':(0, 1),
        'v':(1, 0),
        '<':(0, -1),
        '^':(-1, 0)
    }

    nx = field[0] + move[command][0]
    ny = field[1] + move[command][1]
    if grid[nx,ny] in ['.']:
        return 1
    elif grid[nx,ny] in ['#']:
        return -1
    elif grid[nx,ny] in ['[',']']:
        return can_be_moved(grid,(nx,ny), command)
    else:
        return None # ERROR

def attempt_move_part2(grid, field, command):
    move = {
        '>':(0, 1),
        'v':(1, 0),
        '<':(0, -1),
        '^':(-1, 0)
    }

    nx = field[0] + move[command][0]
    ny = field[1] + move[command][1]
    
    can_move = -1  # default to can't move

    # print(f'Next position = ({nx, ny})')
    if grid[nx,ny] in ['.']:  # can move to empty space or current position
        grid[nx,ny] = grid[field]
        grid[field] = '.'  # clear original position
        can_move = 1

    elif grid[nx,ny] in ['[']:  
        if can_be_moved(grid,(nx,ny+1), command)>0 and can_be_moved(grid,(nx,ny), command)>0:
            moved_first = attempt_move_part2(grid,(nx,ny+1), command) # need try to move ']' first !!
            moved = attempt_move_part2(grid,(nx,ny), command) # now move the second part
            # next moved --> can move now
            grid[nx,ny] = grid[field]
            grid[field] = '.'  # clear original position
            can_move = 1           
    
    elif grid[nx,ny] in [']']:  # try to move that field first
        if can_be_moved(grid,(nx,ny-1), command)>0 and can_be_moved(grid,(nx,ny), command)>0:
            moved_first = attempt_move_part2(grid,(nx,ny-1), command) 
            moved = attempt_move_part2(grid,(nx,ny), command) # now move the second part
            # next moved --> can move now
            grid[nx,ny] = grid[field]
            grid[field] = '.'  # clear original position
            can_move = 1
    # else: it's a wall or something else, keep can_move as -1
    
    return can_move


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
    grid_transformed = np.full((rows, 2*cols),'.', dtype='<U1')  # <U1 ensures single-character strings
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
            else:
                pass # ERROR     
    return grid_transformed

def solve_part1(grid, commands) -> int:
    """
    Solve part 1 of the puzzle.
    
    Args:
        data: Puzzle input

    Returns:
        Solution to part 1
    """
    robot_position = np.where(grid == '@')
    x, y = (robot_position[0][0], robot_position[1][0])

    for step, command in enumerate(commands):
        if attempt_move(grid, (x,y), command)>0:
            # DEBUG: print('Moved')
            # Update position after successful move
            robot_position = np.where(grid == '@')
            x, y = (robot_position[0][0], robot_position[1][0])
        else: 
            pass
            #  DEDUG: print('No move')

        # print(f'After step = {step}, command = {command}. Grid:')
        # print(grid)
        

    return calc_grid_value(grid)

def solve_part2(grid, commands) -> int:
    """
    Solve part 2 of the puzzle.
    
    Args:
        data: Puzzle input

    Returns:
        Solution to part 2
    """
    # calc transformed grid
    grid2 = transform_grid_part2(grid)

    robot_position = np.where(grid2 == '@')
    x, y = (robot_position[0][0], robot_position[1][0])

    # print('Initial position:')
    # print(f'Robot: {x,y}, commands to do: {len(commands)}')
    # print(grid2)
    # print('---------')
    

    for step, command in enumerate(commands):
        # print(f'Command == {command}')
        if attempt_move_part2(grid2, (x,y), command)>0:
            # print('Moved')
            # print('New Grid:')
            # print(grid2)
            # Update position after successful move
            robot_position = np.where(grid2 == '@')
            x, y = (robot_position[0][0], robot_position[1][0])
        else: 
            # print('Not Moved')
            pass

    return calc_grid_value(grid2)

def main():
    # Read the input
    data = read_lines(15)
    
    # Parse the input
    grid, commands = parse_input(data)
    
    # Solve part 1
    part1_result = solve_part1(grid, commands)
    print(f"Part 1: {part1_result}")
    
    print('Starting part 2:')
    # Solve part 2
    part2_result = solve_part2(grid, commands)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
