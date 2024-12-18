from src.utils.input_reader import read_lines
import random

class Computer:
    def __init__(self, a=0, b=0, c=0):
        self.registers = {'A': a, 'B': b, 'C': c}
        self.ip = 0
        self.outputs = []
        self.program = []
        self.debug = False
        self.max_steps = 1000000
        
    def get_combo_value(self, operand):
        if operand <= 3:
            return operand
        elif operand == 4:
            return self.registers['A']
        elif operand == 5:
            return self.registers['B']
        elif operand == 6:
            return self.registers['C']
        else:
            raise ValueError(f"Invalid combo operand: {operand}")
    
    def adv(self, operand, target='A'):
        numerator = self.registers['A']
        denominator = 2 ** self.get_combo_value(operand)
        self.registers[target] = numerator // denominator
        self.ip += 2
    
    def bxl(self, operand):
        self.registers['B'] ^= operand
        self.ip += 2
    
    def bst(self, operand):
        value = self.get_combo_value(operand) % 8
        self.registers['B'] = value
        self.ip += 2
    
    def jnz(self, operand):
        if self.registers['A'] != 0:
            self.ip = operand
        else:
            self.ip += 2
    
    def bxc(self, operand):
        self.registers['B'] ^= self.registers['C']
        self.ip += 2
    
    def out(self, operand):
        value = self.get_combo_value(operand) % 8
        self.outputs.append(str(value))
        self.ip += 2
    
    def bdv(self, operand):
        self.adv(operand, 'B')
    
    def cdv(self, operand):
        self.adv(operand, 'C')
    
    def execute_instruction(self):
        if self.ip >= len(self.program):
            return False
            
        opcode = self.program[self.ip]
        operand = self.program[self.ip + 1]
        
        instructions = {
            0: self.adv,
            1: self.bxl,
            2: self.bst,
            3: self.jnz,
            4: self.bxc,
            5: self.out,
            6: self.bdv,
            7: self.cdv
        }
        
        instructions[opcode](operand)
        return True
    
    def run(self, max_outputs=None):
        self.outputs = []
        self.ip = 0
        steps = 0
        while self.execute_instruction():
            steps += 1
            if steps > self.max_steps:
                break
            if max_outputs and len(self.outputs) >= max_outputs:
                break
        return ','.join(self.outputs)

def parse_input(data):
    registers = {}
    for line in data[:3]:
        reg, value = line.split(': ')
        registers[reg[-1]] = int(value)
    
    program = [int(x) for x in data[-1].split(': ')[1].split(',')]
    return registers, program

def solve_part1(data) -> str:
    registers, program = parse_input(data)
    computer = Computer(registers['A'], registers['B'], registers['C'])
    computer.program = program
    return computer.run()

def get_sequence_info(a, program):
    computer = Computer(a, 0, 0)
    computer.program = program
    output = computer.run()
    nums = [int(x) for x in output.split(',')]
    return len(nums), nums

def count_matching_digits(seq1, seq2):
    """Count how many digits match from the start"""
    count = 0
    for a, b in zip(seq1, seq2):
        if a != b:
            break
        count += 1
    return count

def try_random_values(program, num_tries=10000000):
    """Try random values and track best examples for each match length"""
    min_val = int(3.5 * (10 ** 13))
    max_val = int(28.15 * (10 ** 13))
    target = [2,4,1,5,7,5,1,6,4,3,5,5,0,3,3,0]
    
    print(f"Target sequence: {target}")
    print(f"Trying {num_tries:,} random values between {min_val} and {max_val}")
    print("-" * 50)
    
    # Track best example for each number of matching digits
    best_examples = {}  # key: num_matching, value: (A, sequence)
    
    for i in range(num_tries):
        # Progress indicator every 100k tries
        if i > 0 and i % 100000 == 0:
            print(f"Processed {i:,} values. Found examples for {len(best_examples)} different match lengths")
        
        # Generate random A value in range
        a = random.randint(min_val, max_val)
        length, nums = get_sequence_info(a, program)
        
        # Only interested in sequences of length 16
        if length == 16:
            matching = count_matching_digits(nums, target)
            
            # If this is the best example for this number of matching digits
            if matching > 0 and (matching not in best_examples or a < best_examples[matching][0]):
                best_examples[matching] = (a, nums)
                print(f"\nNew example for {matching} matching digits:")
                print(f"A = {a}")
                print(f"Sequence: {nums}")
    
    print("\nBest examples found for each number of matching digits:")
    print("-" * 50)
    for matching in sorted(best_examples.keys()):
        a, sequence = best_examples[matching]
        print(f"\n{matching} matching digits:")
        print(f"A = {a}")
        print(f"Sequence: {sequence}")
        print(f"Target:   {target}")
        print(f"Match:    {''.join(['✓' if a==b else '✗' for a,b in zip(sequence, target)])}")
    
    return best_examples

def solve_part2(data) -> int:
    _, program = parse_input(data)
    try_random_values(program)
    return 0  # Placeholder return since we're just searching

def main():
    data = read_lines(17)
    
    # Solve part 1
    part1_result = solve_part1(data)
    print(f"Part 1: {part1_result}")
    
    # Solve part 2
    part2_result = solve_part2(data)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
