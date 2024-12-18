from src.utils.input_reader import read_lines

class Computer:
    def __init__(self, a=0, b=0, c=0):
        self.registers = {'A': a, 'B': b, 'C': c}
        self.ip = 0
        self.outputs = []
        self.program = []
        
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
        self.outputs.append(value)
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
        while self.execute_instruction():
            if max_outputs and len(self.outputs) >= max_outputs:
                break
        return self.outputs

def solve_part1(data):
    registers = {}
    for line in data[:3]:
        reg, value = line.split(': ')
        registers[reg[-1]] = int(value)
    
    program = [int(x) for x in data[-1].split('Program: ')[1].split(',')]
    
    computer = Computer(registers['A'], registers['B'], registers['C'])
    computer.program = program
    outputs = computer.run()
    return ','.join(map(str, outputs))

def find_valid_10bit_values(target_output, program, position):
    """Find 10-bit values that produce target output at given position"""
    valid_values = []
    
    # Try all possible 10-bit values
    for i in range(1024):  # 2^10
        # Place these 10 bits at the correct position
        value = i << (position * 3)
        # Add minimum octal value to ensure 16 digits
        min_octal = int('1' + '0' * 15, 8)
        test_value = min_octal | value
        
        computer = Computer(test_value, 0, 0)
        computer.program = program
        outputs = computer.run(position + 1)
        
        if len(outputs) > position and outputs[position] == target_output:
            valid_values.append(i)
            print(f"Found value {bin(i)[2:].zfill(10)} for output {target_output} at position {position}")
    
    return valid_values

def solve_part2(data):
    """Find input value by analyzing 10-bit windows"""
    target = [2,4,1,5,7,5,1,6,4,3,5,5,0,3,3,0]  # Desired output sequence
    _, program = parse_input(data)
    
    # Find valid 10-bit values for each position
    valid_values = []
    for i, t in enumerate(target):
        print(f"\nFinding values for output {t} at position {i}")
        values = find_valid_10bit_values(t, program, i)
        if not values:
            print(f"No valid values found for output {t} at position {i}")
            return None
        valid_values.append(values)
        print(f"Found {len(values)} valid values")
    
    # Try combining valid values
    def try_combination(pos=0, value=0):
        if pos == len(target):
            # Verify complete solution
            computer = Computer(value, 0, 0)
            computer.program = program
            outputs = computer.run()
            if outputs == target:
                return value
            return None
        
        for v in valid_values[pos]:
            # Add these bits to our value
            new_value = value | (v << (pos * 3))
            # Test if this combination works so far
            computer = Computer(new_value, 0, 0)
            computer.program = program
            outputs = computer.run(pos + 1)
            if outputs == target[:pos + 1]:
                result = try_combination(pos + 1, new_value)
                if result is not None:
                    return result
        return None
    
    # Find solution
    result = try_combination()
    
    if result:
        print("\nVerifying solution:")
        print(f"Final value (decimal): {result}")
        print(f"Final value (octal): {oct(result)[2:]}")
        computer = Computer(result, 0, 0)
        computer.program = program
        outputs = computer.run()
        print(f"Target sequence: {target}")
        print(f"Actual outputs: {outputs}")
        print(f"Matches: {outputs == target}")
    
    return result

def parse_input(data):
    registers = {}
    for line in data[:3]:
        reg, value = line.split(': ')
        registers[reg[-1]] = int(value)
    
    program = [int(x) for x in data[-1].split('Program: ')[1].split(',')]
    return registers, program

def main():
    data = read_lines(17)
    
    part1_result = solve_part1(data)
    print(f"Part 1: {part1_result}")
    
    part2_result = solve_part2(data)
    print(f"Part 2: {part2_result}")

if __name__ == "__main__":
    main()
