import importlib
import sys
from typing import Optional

def run_day(day: int, part: Optional[int] = None):
    """
    Run solutions for a specific day.
    If part is specified, run only that part. Otherwise, run both parts.
    """
    # Pad day number with leading zero if needed
    day_str = str(day).zfill(2)
    
    try:
        # Dynamically import the day's solution module
        solution_module = importlib.import_module(f'src.solutions.day{day_str}')
        
        # Execute the main function
        solution_module.main()
        
    except ImportError as e:
        print(f"No solution found for day {day}")
        print(f"Error: {e}")
    except Exception as e:
        print(f"Error running day {day}: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print("Please provide a day number to run")
        print("Usage: python main.py <day_number>")
        return
    
    try:
        day = int(sys.argv[1])
        if day < 1 or day > 25:
            print("Day must be between 1 and 25")
            return
        
        run_day(day)
        
    except ValueError:
        print("Please provide a valid day number")

if __name__ == "__main__":
    main()
