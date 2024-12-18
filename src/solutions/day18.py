import numpy as np
from src.utils.input_reader import read_lines, read_numbers

def print_matrix(matrix:np.ndarray):
    for row in matrix:
        print(' '.join(map(str,row)))
    return

def find_all_neighbours(w:np.ndarray[int], corrupted: np.ndarray[str], steps:int):
    DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    
    l = np.argwhere(w == steps)
    
    rows,cols = w.shape

    res = []

    for e in l:
        if corrupted[e[0],e[1]]!='#':
            for d in DIRECTIONS:
                nx,ny = e[0]+d[0],e[1]+d[1]
                if 0<=nx<rows and 0<=ny<cols and w[nx,ny]==0:
                    res.append((nx,ny))
    return res

def solve_part1(data, is_part_two_call=False) -> int:
    """
    Solve part 1 of the puzzle.
    
    Args:
        data: Puzzle input

    Returns:
        Solution to part 1
    """
    data = [list(map(int,e.split(','))) for e in data]
    
    size = 71
    matrix = np.full((size, size), '.', dtype=str)  # Initialize with dtype=str
    w = np.zeros((size, size), dtype=int)

    # Mark corrupted bytes
    if is_part_two_call:
        max = len(data)
    else:
        max = 1024

    for i in range(max):
        x,y = data[i]  # Now correctly using x,y order
        matrix[y,x] = '#'  # Using y,x for numpy array indexing
        w[y,x] = -1

    # debug: print('Current stones field:')
    # print_matrix(matrix)
    print(f'Running at stones count on the field ={max}, last stone added = {data[-1]}')
    # Find optimal path
    step = 1
    v = [(0,0)]
    while w[size-1,size-1]==0 and step<=size*size:
        for e in v: 
            w[e[0],e[1]]= step
        v = find_all_neighbours(w, corrupted=matrix, steps=step)
        is_end_close=[e for e in v if e[0]==size-1 and e[1]==size-1]
        if len(v)==0 and not is_end_close and w[size-1,size-1]==0:
            return -1 
        step+=1

    return w[size-1,size-1]-1

def solve_part2(data) -> int:
    """
    Solve part 2 of the puzzle.
    
    Args:
        data: Puzzle input

    Returns:
        Solution to part 2
    """
    max = len(data)
    print(f'Max stones to come {max}')

    for cur in range(max):
        solve = solve_part1(data[0:cur+1], is_part_two_call=True)
        print(f'Answer: min steps to reach exit = {solve}. If it is >-1, then the path is still not blocked')
        print('-------')
        if solve==-1:
            return data[cur]

    return 'No solution'

def main():
    data = read_lines(18)
    
    part1_result = solve_part1(data)
    print(f"Part 1: {part1_result}")
    
    part2_result = solve_part2(data)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
