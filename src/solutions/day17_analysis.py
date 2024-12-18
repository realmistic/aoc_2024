from day17 import Computer

def get_sequence_info(a):
    computer = Computer(a, 0, 0)
    computer.program = [2,4,1,5,7,5,1,6,4,3,5,5,0,3,3,0]
    output = computer.run()
    nums = [int(x) for x in output.split(',')]
    return len(nums), nums[:3] if nums else []

def find_length_pattern():
    print("Finding sequence length pattern...")
    print("-" * 50)
    
    target_length = 16
    current_length = 0
    power = 10  # Start at 2^10
    
    while power < 100:  # Go up to 2^100 if needed
        base = 2 ** power
        length, start = get_sequence_info(base)
        
        print(f"\n2^{power} = {base}")
        print(f"Length: {length}, Starts with: {start}")
        
        if length >= target_length:
            print(f"Found sequence of target length!")
            return
            
        # Try exponentially increasing multipliers
        multipliers = []
        mult = 3
        while mult * base < (2 ** (power + 1)):
            multipliers.append(mult)
            mult *= 2
        
        # Try each multiplier
        for mult in multipliers:
            mult_a = base * mult
            mult_length, mult_start = get_sequence_info(mult_a)
            print(f"2^{power} * {mult} = {mult_a}")
            print(f"Length: {mult_length}, Starts with: {mult_start}")
            
            if mult_length >= target_length:
                print(f"Found sequence of target length!")
                return
                
            if mult_length > length:
                print(f"Found longer sequence with multiplier {mult}!")
        
        # Also try adding/subtracting small numbers
        for offset in [-1, 1, -7, 7, -11, 11]:
            off_a = base + offset
            off_length, off_start = get_sequence_info(off_a)
            if off_length > length:
                print(f"\n2^{power} {offset:+d} = {off_a}")
                print(f"Length: {off_length}, Starts with: {off_start}")
        
        power += 1
        if power % 5 == 0:  # Print separator every 5 powers
            print("\n" + "=" * 50)

def main():
    target = [2,4,1,5,7,5,1,6,4,3,5,5,0,3,3,0]
    print(f"Target sequence length: {len(target)}")
    print(f"Target starts with: {target[:3]}")
    print("=" * 50)
    
    find_length_pattern()

if __name__ == "__main__":
    main()
