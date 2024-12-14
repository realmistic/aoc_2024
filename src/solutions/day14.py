from typing import List, Tuple
from statistics import stdev, mean
from src.utils.input_reader import read_lines

def parse_robot(line: str) -> Tuple[int, int, int, int]:
    """Parse a line like 'p=0,4 v=3,-3' into (x, y, dx, dy)"""
    pos_part, vel_part = line.split()
    pos_x, pos_y = map(int, pos_part[2:].split(','))
    vel_x, vel_y = map(int, vel_part[2:].split(','))
    return (pos_x, pos_y, vel_x, vel_y)

def calculate_pos(robot: Tuple[int, int, int, int], width: int, height: int, t: int) -> Tuple[int, int]:
    """Calculate position at time t with wrapping"""
    x, y, dx, dy = robot
    return (x + dx * t) % width, (y + dy * t) % height

def print_grid(robots: List[Tuple[int, int, int, int]], width: int, height: int, t: int):
    """Print current robot positions"""
    positions = [calculate_pos(robot, width, height, t) for robot in robots]
    
    # Find bounds of occupied positions
    min_x = max(0, min(x for x, _ in positions) - 1)
    max_x = min(width, max(x for x, _ in positions) + 2)
    min_y = max(0, min(y for _, y in positions) - 1)
    max_y = min(height, max(y for _, y in positions) + 2)
    
    print(f"\nRobot positions at time {t}:")
    for y in range(min_y, max_y):
        row = f"{y:2d} "
        for x in range(min_x, max_x):
            count = positions.count((x, y))
            if count > 0:
                row += '#'  # Use '#' for robots
            else:
                row += '.'  # Use '.' for empty space
        print(row)
    print()

def compute_safety_factor(robots: List[Tuple[int, int, int, int]], width: int, height: int, t: int) -> int:
    """Calculate safety factor (multiply quadrant counts)"""
    positions = [calculate_pos(robot, width, height, t) for robot in robots]
    
    limit_x, limit_y = (width - 1) / 2, (height - 1) / 2
    
    # Count robots in each quadrant
    tl = sum(1 for x, y in positions if x < limit_x and y < limit_y)
    tr = sum(1 for x, y in positions if x > limit_x and y < limit_y)
    bl = sum(1 for x, y in positions if x < limit_x and y > limit_y)
    br = sum(1 for x, y in positions if x > limit_x and y > limit_y)
    
    print("Robots in quadrants:", tl, tr, bl, br)
    return tl * tr * bl * br

def find_christmas_tree(robots: List[Tuple[int, int, int, int]], width: int, height: int) -> int:
    """Find time when robots form Christmas tree pattern using clustering detection"""
    t = 1
    dt = 1  # Start with horizontal clustering
    iterations = []
    
    while True:
        # Get current positions
        positions = [calculate_pos(robot, width, height, t) for robot in robots]
        x_coords = [x for x, _ in positions]
        y_coords = [y for _, y in positions]
        
        # Check clustering based on current phase
        if dt == 1:
            # Looking for horizontal clustering
            cluster_value = stdev(x_coords)
        else:
            # Looking for vertical clustering
            cluster_value = stdev(y_coords)
        
        iterations.append(cluster_value)
        mean_cluster = mean(iterations)
        
        # Print current state periodically
        if t % 1000 == 0:
            print(f"Time {t}, cluster value: {cluster_value:.2f}, mean: {mean_cluster:.2f}")
        
        # Check for significant clustering
        if cluster_value < mean_cluster * 0.8:
            if dt == 1:
                # Found horizontal clustering, switch to vertical
                print(f"Found horizontal clustering at time {t}")
                print_grid(robots, width, height, t)
                iterations = [stdev(y_coords)]  # Reset for vertical phase
                dt = width
            else:
                # Found both clusterings
                print(f"Found complete pattern at time {t}")
                print_grid(robots, width, height, t)
                return t
        
        if t > 10000:
            print("No pattern found within time limit")
            return -1
            
        t += dt

def solve_part1(robots: List[Tuple[int, int, int, int]], width: int, height: int, seconds: int) -> int:
    """Calculate safety factor after given number of seconds"""
    return compute_safety_factor(robots, width, height, seconds)

def solve_part2(robots: List[Tuple[int, int, int, int]], width: int, height: int) -> int:
    """Find time when robots form Christmas tree pattern"""
    return find_christmas_tree(robots, width, height)

def main():
    lines = read_lines(14)
    
    # Parse robots
    robots = [parse_robot(line) for line in lines]
    print(f"Total robots: {len(robots)}")
    
    # Part 1: Calculate safety factor at 100 seconds
    part1_result = solve_part1(robots, width=101, height=103, seconds=100)
    print(f"Part 1: {part1_result}")
    
    # Part 2: Find Christmas tree pattern
    part2_result = solve_part2(robots, width=101, height=103)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
