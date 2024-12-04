import os
import sys
import numpy as np
from typing import List, Tuple

# Add the project root directory to Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
if project_root not in sys.path:
    sys.path.append(project_root)

from src.utils.input_reader import read_lines

def get_sequences_from_position(array: np.ndarray, i: int, j: int, length: int = 4) -> List[Tuple[str, str]]:
    """
    Get all possible sequences of specified length starting from position (i,j) in all directions.
    
    Args:
        array: 2D numpy array of characters
        i: row index
        j: column index
        length: length of sequences to extract (default 4)
    
    Returns:
        List of tuples (sequence, direction), where sequence is a string and direction describes how it was extracted
    """
    height, width = array.shape
    sequences = []
    
    # Define all possible directions as (di, dj, direction_name)
    directions = [
        (0, 1, "right"),    # right
        (0, -1, "left"),    # left
        (1, 0, "down"),     # down
        (-1, 0, "up"),      # up
        (1, 1, "down-right"),   # diagonal down-right
        (-1, -1, "up-left"),    # diagonal up-left
        (1, -1, "down-left"),   # diagonal down-left
        (-1, 1, "up-right")     # diagonal up-right
    ]
    
    for di, dj, direction in directions:
        sequence = []
        valid = True
        
        # Try to build sequence of required length
        for step in range(length):
            new_i = i + di * step
            new_j = j + dj * step
            
            # Check if position is valid
            if 0 <= new_i < height and 0 <= new_j < width:
                sequence.append(array[new_i, new_j])
            else:
                valid = False
                break
        
        # If we got a valid sequence of required length, add it
        if valid and len(sequence) == length:
            sequences.append((''.join(sequence), direction))
    
    return sequences

def check_xmas_sequence(sequence: str) -> int:
    """
    Check if a sequence matches 'XMAS'.
    
    Args:
        sequence: String to check
    
    Returns:
        1 if sequence matches 'XMAS', 0 otherwise
    """
    return 1 if sequence == "XMAS" else 0

def find_xmas_at_position(array: np.ndarray, i: int, j: int) -> List[Tuple[int, str]]:
    """
    Find all XMAS sequences starting from position (i,j).
    
    Args:
        array: 2D numpy array of characters
        i: row index
        j: column index
    
    Returns:
        List of tuples (match_result, direction), where match_result is 0 or 1
    """
    sequences = get_sequences_from_position(array, i, j)
    return [(check_xmas_sequence(seq), direction) for seq, direction in sequences]

def count_all_xmas_matches(array: np.ndarray) -> int:
    """
    Count total number of XMAS matches in the array from all possible starting positions.
    
    Args:
        array: 2D numpy array of characters
    
    Returns:
        Total number of XMAS matches found
    """
    height, width = array.shape
    total_matches = 0
    matches_found = []
    
    # Check every position in the array
    for i in range(height):
        for j in range(width):
            results = find_xmas_at_position(array, i, j)
            for match, direction in results:
                if match:
                    total_matches += 1
                    matches_found.append((i, j, direction))
    
    # Print detailed match information
    print("\nFound XMAS matches at:")
    for i, j, direction in matches_found:
        print(f"Position ({i},{j}) in direction {direction}")
    
    return total_matches

def check_pattern_at_position(array: np.ndarray, i: int, j: int) -> List[str]:
    """
    Check if any of the 3x3 pattern rotations match at position (i,j).
    
    Args:
        array: 2D numpy array of characters
        i: row index
        j: column index
    
    Returns:
        List of matching pattern rotations
    """
    height, width = array.shape
    matches = []
    
    # Skip if we can't fit a 3x3 pattern at this position
    if i + 2 >= height or j + 2 >= width:
        return matches
    
    # Get the 3x3 subarray at this position
    subarray = array[i:i+3, j:j+3]
    
    # Define all pattern rotations (only checking fixed positions, . can be any char)
    patterns = [
        # 0 degrees
        [(0,0,'M'), (0,2,'S'), (1,1,'A'), (2,0,'M'), (2,2,'S')],
        # 90 degrees
        [(0,0,'M'), (0,2,'M'), (1,1,'A'), (2,0,'S'), (2,2,'S')],
        # 180 degrees
        [(0,0,'S'), (0,2,'M'), (1,1,'A'), (2,0,'S'), (2,2,'M')],
        # 270 degrees
        [(0,0,'S'), (0,2,'S'), (1,1,'A'), (2,0,'M'), (2,2,'M')]
    ]
    
    # Check each rotation pattern
    rotation_names = ["0°", "90°", "180°", "270°"]
    for pattern, rotation in zip(patterns, rotation_names):
        matches_pattern = True
        for pi, pj, char in pattern:
            if subarray[pi, pj] != char:
                matches_pattern = False
                break
        if matches_pattern:
            matches.append(rotation)
    
    return matches

def find_all_pattern_matches(array: np.ndarray):
    """
    Find all matches of the 3x3 pattern in all rotations.
    """
    height, width = array.shape
    matches_found = []
    
    # Check every possible 3x3 window position
    for i in range(height-2):  # -2 to leave room for 3x3 pattern
        for j in range(width-2):
            rotations = check_pattern_at_position(array, i, j)
            if rotations:
                matches_found.append((i, j, rotations))
    
    # Print results
    print("\nFound pattern matches:")
    for i, j, rotations in matches_found:
        print(f"Position ({i},{j}):")
        print("3x3 pattern found:")
        for row in array[i:i+3, j:j+3]:
            print(''.join(row))
        print(f"Matching rotations: {', '.join(rotations)}\n")
    
    return len(matches_found)

def parse_input(data):
    """Parse the input into a numpy array of characters."""
    # Convert input lines to list of character lists
    char_list = [list(line.strip()) for line in data]
    return np.array(char_list)

def solve_part1(data) -> int:
    """
    Solve part 1 of the puzzle.
    
    Args:
        data: List of strings, each containing a sequence of M, S, A, X characters

    Returns:
        Solution to part 1
    """
    # Convert input to numpy array
    char_array = parse_input(data)
    
    # Count all XMAS matches in the array
    total_matches = count_all_xmas_matches(char_array)
    print(f"\nTotal XMAS matches found: {total_matches}")
    
    return total_matches

def solve_part2(data) -> int:
    """
    Solve part 2 of the puzzle.
    
    Args:
        data: List of strings, each containing a sequence of M, S, A, X characters

    Returns:
        Solution to part 2
    """
    # Convert input to numpy array
    char_array = parse_input(data)
    
    # Find all 3x3 pattern matches
    total_matches = find_all_pattern_matches(char_array)
    print(f"\nTotal 3x3 pattern matches found: {total_matches}")
    
    return total_matches

def main():
    # Read data from 4.txt
    data = read_lines(4)
    
    # Solve part 1
    part1_result = solve_part1(data)
    print(f"\nPart 1: {part1_result}")
    
    # Solve part 2
    part2_result = solve_part2(data)
    print(f"\nPart 2: {part2_result}")

if __name__ == "__main__":
    main()
