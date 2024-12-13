def read_lines(day: int) -> list[str]:
    """Read input file for given day and return lines."""
    with open(f'inputs/{day}.txt', 'r') as file:
        return [line.strip() for line in file]

def read_numbers(day: int) -> list[list[int]]:
    """Read input file for given day and return numbers from each line."""
    with open(f'inputs/{day}.txt', 'r') as file:
        return [[int(x) for x in line.strip().split()] for line in file]

def read_chars(day: int) -> list[str]:
    """Read input file for the given day and return characters as a list."""
    with open(f'inputs/{day}.txt', 'r') as file:
        return list(file.read().strip())

def read_char_matrix(day: int) -> list[list[str]]:
    """Read input file for given day and return matrix of chars."""
    with open(f'inputs/{day}.txt', 'r') as file:
        return [list(line.strip()) for line in file]
