from src.utils.input_reader import read_lines
from collections import defaultdict
from typing import List, Tuple, Set

def get_antenna_positions(grid: List[str]) -> defaultdict:
    """Find all antenna positions grouped by frequency."""
    antennas = defaultdict(list)
    for y, row in enumerate(grid):
        for x, char in enumerate(row):
            if char != '.':
                antennas[char].append((x, y))
    return antennas

def is_collinear(p1: Tuple[int, int], p2: Tuple[int, int], p3: Tuple[int, int]) -> bool:
    """Check if three points are in a straight line."""
    x1, y1 = p1
    x2, y2 = p2
    x3, y3 = p3
    # Calculate area of triangle formed by three points
    # If area is 0, points are collinear
    return (x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) == 0

def find_points_on_line(a1: Tuple[int, int], a2: Tuple[int, int], grid_width: int, grid_height: int) -> List[Tuple[int, int]]:
    """Find all grid points that lie on the line between and beyond two points."""
    x1, y1 = a1
    x2, y2 = a2
    points = set()  # Use set to avoid duplicates
    
    # Add the antenna points themselves
    points.add(a1)
    points.add(a2)
    
    # Calculate direction vector
    dx = x2 - x1
    dy = y2 - y1
    
    # Normalize the direction vector to get the smallest step
    if dx != 0 and dy != 0:
        gcd = abs(dx)
        for i in range(1, abs(dy) + 1):
            if dx % i == 0 and dy % i == 0:
                gcd = i
        dx //= gcd
        dy //= gcd
    elif dx != 0:
        dx = dx // abs(dx)
    elif dy != 0:
        dy = dy // abs(dy)
    
    # Start from first antenna and move in both directions
    x, y = x1, y1
    # Move forward
    while 0 <= x < grid_width and 0 <= y < grid_height:
        if is_collinear(a1, a2, (x, y)):
            points.add((x, y))
        x += dx
        y += dy
    
    # Move backward
    x, y = x1 - dx, y1 - dy
    while 0 <= x < grid_width and 0 <= y < grid_height:
        if is_collinear(a1, a2, (x, y)):
            points.add((x, y))
        x -= dx
        y -= dy
    
    return list(points)

def solve_part2(data: List[str], debug: bool = False) -> int:
    """
    Solve part 2 of the puzzle.
    
    Args:
        data: Grid showing antenna positions
        debug: Whether to print debug information

    Returns:
        Number of unique antinode locations
    """
    # Get antenna positions grouped by frequency
    antennas = get_antenna_positions(data)
    grid_width = len(data[0])
    grid_height = len(data)
    
    if debug:
        print("\nAntenna positions:")
        for freq, pos in antennas.items():
            print(f"Frequency {freq}: {pos}")
    
    # Set to store unique antinode positions
    antinodes = set()
    
    # For each frequency with multiple antennas
    for freq, positions in antennas.items():
        if len(positions) < 2:
            continue
            
        if debug:
            print(f"\nProcessing frequency: {freq}")
        
        # Add antenna positions themselves as antinodes
        for pos in positions:
            antinodes.add(pos)
        
        # Check all pairs of antennas
        for i in range(len(positions)):
            for j in range(i + 1, len(positions)):
                # Find all points on the line between these antennas
                line_points = find_points_on_line(
                    positions[i], 
                    positions[j],
                    grid_width,
                    grid_height
                )
                
                if debug:
                    print(f"Line between {positions[i]} and {positions[j]} contains points: {sorted(line_points)}")
                
                # All points on the line are antinodes
                antinodes.update(line_points)
    
    if debug:
        print("\nFinal grid with antinodes (#):")
        result = []
        for y in range(len(data)):
            row = list(data[y])
            for x in range(len(row)):
                if (x, y) in antinodes and row[x] == '.':
                    row[x] = '#'
            result.append(''.join(row))
        for row in result:
            print(row)
    
    return len(antinodes)

def main():
    # Test with example input
    example = [
        "............",
        "........0...",
        ".....0......",
        ".......0....",
        "....0.......",
        "......A.....",
        "............",
        "............",
        "........A...",
        ".........A..",
        "............",
        "............"
    ]
    example_result = solve_part2(example, debug=True)
    print(f"\nExample result: {example_result} (should be 34)")
    
    # Solve with actual input
    print("\nSolving actual input:")
    data = read_lines(8)
    part2_result = solve_part2(data)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
