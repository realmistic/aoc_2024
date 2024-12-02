# Advent of Code 2024

Solutions for Advent of Code 2024 challenges.

## Project Structure

```
.
├── inputs/          # Input files for each day
│   ├── 1.txt
│   ├── 2.txt
│   └── ...
├── src/            # Source code
│   ├── solutions/  # Daily solutions
│   │   ├── __init__.py
│   │   ├── day01.py
│   │   ├── day02.py
│   │   └── ...
│   ├── utils/     # Utility functions
│   │   ├── __init__.py
│   │   └── input_reader.py
│   └── main.py    # Main runner script
├── requirements.txt # Project dependencies
└── README.md
```

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
```

2. Activate the virtual environment:
```bash
# On Windows:
venv\Scripts\activate

# On Unix or MacOS:
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

To run a solution for a specific day:

```bash
python src/main.py <day_number>
```

For example, to run day 1's solution:

```bash
python src/main.py 1
```

## Solution Structure

Each day's solution follows the same pattern:

1. Solutions are placed in `src/solutions/dayXX.py`
2. Input files are placed in `inputs/X.txt`
3. Each solution file contains:
   - `solve_part1()` function for part 1
   - `solve_part2()` function for part 2
   - `main()` function to run both parts

## Adding New Solutions

1. Create a new solution file in `src/solutions/` following the naming pattern `dayXX.py`
2. Place your input file in `inputs/` as `X.txt`
3. Implement the required functions:
   - `solve_part1()`
   - `solve_part2()`
   - `main()`
4. Run your solution using `python src/main.py X` where X is the day number

## Utilities

The `utils` package provides common functionality:

- `input_reader.py`: Functions for reading input files
  - `read_lines()`: Read input file as lines of text
  - `read_numbers()`: Read input file as lists of numbers
