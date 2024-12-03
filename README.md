# Advent of Code 2024

Solutions for Advent of Code 2024 challenges.

## Project Structure

```
.
├── inputs/                # Input files for each day
│   ├── template_input.txt # Template with common input patterns
│   ├── 1.txt
│   ├── 2.txt
│   └── ...
├── src/                  # Source code
│   ├── solutions/        # Daily solutions
│   │   ├── template_solution.py  # Template for new solutions
│   │   ├── day01.py
│   │   ├── day02.py
│   │   └── ...
│   ├── utils/           # Utility functions
│   │   ├── __init__.py
│   │   └── input_reader.py
│   └── main.py          # Main runner script
├── requirements.txt      # Project dependencies
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

## Adding New Solutions

1. Copy the template files:
   - Copy `src/solutions/template_solution.py` to `src/solutions/dayXX.py`
   - Reference `inputs/template_input.txt` for common input patterns
   - Create `inputs/X.txt` for your puzzle input

2. Update the solution file:
   - Change the day number in `read_lines(0)` to your day number
   - Choose appropriate input reader (`read_lines()` or `read_numbers()`)
   - Implement `solve_part1()` and `solve_part2()`

3. Run your solution:
   ```bash
   python src/main.py X  # where X is the day number
   ```

## Templates

### Solution Template (`template_solution.py`)
- Basic structure for daily solutions
- Includes both part 1 and part 2 functions
- Configurable input reading
- Ready-to-use main function

### Input Template (`template_input.txt`)
Common input patterns found in Advent of Code:
1. Space-separated numbers
2. Character grids
3. Text instructions
4. Mixed data (numbers and text)
5. Coordinate pairs
6. Binary/hex data

## Utilities

The `utils` package provides common functionality:

- `input_reader.py`: Functions for reading input files
  - `read_lines()`: Read input file as lines of text
  - `read_numbers()`: Read input file as lists of numbers
