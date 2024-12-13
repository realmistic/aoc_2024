from typing import List, Tuple
from src.utils.input_reader import read_lines
import numpy as np

def parse_line(line: str) -> Tuple[int, int]:
    """Parse a line like 'Button A: X+23, Y+33' or 'Prize: X=6801, Y=3810'"""
    parts = line.split(', ')
    x_part = parts[0].split('X')[1].strip('+= ')
    y_part = parts[1].split('Y')[1].strip('+= ')
    return int(x_part), int(y_part)

def parse_input(lines: List[str], prize_offset: int = 0) -> List[Tuple[np.ndarray, np.ndarray]]:
    """Parse input into list of (matrix A, vector y) pairs"""
    entries = []
    i = 0
    while i < len(lines):
        # Parse button A coordinates
        ax, ay = parse_line(lines[i])
        
        # Parse button B coordinates
        bx, by = parse_line(lines[i + 1])
        
        # Parse prize coordinates and add offset if specified
        px, py = parse_line(lines[i + 2])
        if prize_offset:
            px += prize_offset
            py += prize_offset
        
        entries.append(((ax, ay, bx, by), (px, py)))
        i += 4  # Skip blank line
    
    return entries

def solve_2x2_system(a: int, b: int, c: int, d: int, e: int, f: int) -> Tuple[float, float]:
    """
    Solve 2x2 system using Cramer's rule:
    [a b][x] = [e]
    [c d][y]   [f]
    """
    det = a*d - b*c
    if abs(det) < 1e-10:
        return None
        
    x = (e*d - b*f)/det
    y = (a*f - e*c)/det
    
    return x, y

def is_integer(n: float, tolerance: float = 1e-10) -> bool:
    """Check if a number is effectively an integer"""
    return abs(n - round(n)) < tolerance

def verify_solution(a: int, b: int, c: int, d: int, e: int, f: int, t: Tuple[int, int]) -> bool:
    """Verify that the solution satisfies the original equations"""
    t1, t2 = t
    eq1 = abs(a*t1 + b*t2 - e) < 1e-10
    eq2 = abs(c*t1 + d*t2 - f) < 1e-10
    return eq1 and eq2

def solve_equations(entries: List[Tuple[Tuple[int, int, int, int], Tuple[int, int]]], part: int = 1) -> int:
    """Calculate sum of 3*t1 + t2 for all valid integer solutions"""
    total = 0
    equation_num = 1
    
    for (ax, ay, bx, by), (px, py) in entries:
        print(f"\nEquation {equation_num} (Part {part}):")
        print(f"System:")
        print(f"{ax}*t1 + {bx}*t2 = {px}")
        print(f"{ay}*t1 + {by}*t2 = {py}")
        
        result = solve_2x2_system(ax, bx, ay, by, px, py)
        if result is not None:
            t1, t2 = result
            print(f"Raw solution: t1={t1}, t2={t2}")
            
            # Check if solution components are integers
            if is_integer(t1) and is_integer(t2):
                t1, t2 = int(round(t1)), int(round(t2))
                
                # Verify solution
                if verify_solution(ax, bx, ay, by, px, py, (t1, t2)):
                    # Check if solution is valid (positive times)
                    if t1 > 0 and t2 > 0:
                        print(f"Integer solution found: t1={t1}, t2={t2}")
                        value = 3 * t1 + t2
                        print(f"3*t1 + t2 = {value}")
                        total += value
                    else:
                        print(f"No valid solution (negative times: t1={t1}, t2={t2})")
                else:
                    print("Solution verification failed")
            else:
                print("Non-integer solution")
        else:
            print("No solution exists (singular system)")
        
        equation_num += 1
    
    return total

def main():
    lines = read_lines(13)
    
    # Part 1: Normal prize coordinates
    entries = parse_input(lines)
    part1_result = solve_equations(entries, part=1)
    print(f"\nPart 1 result: {part1_result}")
    
    # Part 2: Add 10^13 to prize coordinates
    entries_part2 = parse_input(lines, prize_offset=10**13)
    part2_result = solve_equations(entries_part2, part=2)
    print(f"\nPart 2 result: {part2_result}")

if __name__ == "__main__":
    main()
