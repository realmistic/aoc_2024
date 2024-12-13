from typing import List, Set, Tuple, Dict
from collections import Counter, defaultdict
from src.utils.input_reader import read_lines

def get_neighbors(x: int, y: int, max_x: int, max_y: int) -> List[Tuple[int, int]]:
    neighbors = []
    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        new_x, new_y = x + dx, y + dy
        if 0 <= new_x < max_x and 0 <= new_y < max_y:
            neighbors.append((new_x, new_y))
    return neighbors

def find_region(garden: List[str], x: int, y: int, visited: Set[Tuple[int, int]]) -> Tuple[int, int, Set[Tuple[Tuple[int, int], Tuple[int, int]]]]:
    """Returns (area, perimeter, fence_segments)"""
    if (x, y) in visited:
        return 0, 0, set()
    
    plant_type = garden[y][x]
    max_y, max_x = len(garden), len(garden[0])
    region = set()
    perimeter = 0
    fence_segments = set()  # Set of (cell1, cell2) pairs representing fence segments
    stack = [(x, y)]
    
    while stack:
        curr_x, curr_y = stack.pop()
        if (curr_x, curr_y) in visited:
            continue
            
        visited.add((curr_x, curr_y))
        region.add((curr_x, curr_y))
        
        # Check neighbors
        for nx, ny in get_neighbors(curr_x, curr_y, max_x, max_y):
            if garden[ny][nx] == plant_type:
                if (nx, ny) not in visited:
                    stack.append((nx, ny))
            else:
                perimeter += 1
                # Add fence segment (ordered pair to ensure uniqueness)
                cell1 = min((curr_x, curr_y), (nx, ny))
                cell2 = max((curr_x, curr_y), (nx, ny))
                fence_segments.add((cell1, cell2))
                
        # Check if on edge of garden
        if curr_x == 0:
            perimeter += 1
            fence_segments.add(((curr_x-1, curr_y), (curr_x, curr_y)))
        if curr_x == max_x - 1:
            perimeter += 1
            fence_segments.add(((curr_x, curr_y), (curr_x+1, curr_y)))
        if curr_y == 0:
            perimeter += 1
            fence_segments.add(((curr_x, curr_y-1), (curr_x, curr_y)))
        if curr_y == max_y - 1:
            perimeter += 1
            fence_segments.add(((curr_x, curr_y), (curr_x, curr_y+1)))
            
    return len(region), perimeter, fence_segments

def count_straight_lines(fence_segments: Set[Tuple[Tuple[int, int], Tuple[int, int]]]) -> int:
    """Count number of straight lines by removing adjacent segments."""
    # Convert to mutable list to remove segments
    segments = list(fence_segments)
    straight_lines = 0
    
    # Build adjacency map for quick lookup
    adjacency = defaultdict(set)
    for (x1, y1), (x2, y2) in segments:
        adjacency[(x1, y1)].add((x2, y2))
        adjacency[(x2, y2)].add((x1, y1))
    
    while segments:
        # Take first segment as start of a line
        start, end = segments.pop(0)
        straight_lines += 1
        
        # Remove all adjacent segments that form a straight line
        stack = [(start, end)]
        while stack:
            curr_start, curr_end = stack.pop()
            
            # Remove this segment from adjacency map
            adjacency[curr_start].discard(curr_end)
            adjacency[curr_end].discard(curr_start)
            
            # Check both ends for adjacent segments
            for point in [curr_start, curr_end]:
                # Look for segments that share this point
                for adj_point in list(adjacency[point]):
                    # If segment exists and forms straight line with current segment
                    adj_seg = tuple(sorted([point, adj_point]))
                    if adj_seg in segments:
                        segments.remove(adj_seg)
                        stack.append(adj_seg)
    
    return straight_lines

def solve_part1(garden: List[str]) -> int:
    visited = set()
    total_price = 0
    
    for y in range(len(garden)):
        for x in range(len(garden[0])):
            if (x, y) not in visited:
                area, perimeter, _ = find_region(garden, x, y, visited)
                price = area * perimeter
                total_price += price
                
    return total_price

def solve_part2(garden: List[str]) -> int:
    visited = set()
    total_price = 0
    
    for y in range(len(garden)):
        for x in range(len(garden[0])):
            if (x, y) not in visited and garden[y][x] != '.':
                area, _, fence_segments = find_region(garden, x, y, visited)
                num_lines = count_straight_lines(fence_segments)
                price = area * num_lines
                total_price += price
                
    return total_price

def main():
    garden = read_lines(12)
    
    # Part 1
    part1_result = solve_part1(garden)
    print(f"Part 1: {part1_result}")
    
    # Part 2
    part2_result = solve_part2(garden)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
