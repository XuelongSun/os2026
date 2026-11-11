class Assembler:
    def __init__(self):
        # ADD MORE instructions as needed
        # e.g., SUB, MUL, DIV, STORE, JMP, etc.
        # Must match the CPU instruction set to work correctly
        self.instructions = {
            'LOAD': 0x01,
            'ADD': 0x02, 
        }

        # store the code labels
        self.labels = {}
        # store defined variables
        self.variables = {}
    
    def assemble(self, source):
        # store the code labels
        self.labels = {}
        # store defined variables
        self.variables = {}
        lines = source.splitlines()
        machine_code = []
        address = 0
        # First pass: handle labels and variables
        for line in lines:
            line = line.split(';')[0].strip()  # Remove comments
            if not line:
                continue
            
            if ':' in line:
                parts = line.split(':')
                # variable definitions
                if parts[1].strip():
                    label = parts[0].strip()
                    value_str = parts[1].split(';')[0].strip()
                    if value_str.startswith('0x'):
                        self.variables[label] = int(value_str, 16)
                    elif value_str.startswith('0b'):
                        self.variables[label] = int(value_str, 2)
                    elif value_str.isdigit():
                        self.variables[label] = int(value_str)
                    else:
                        raise ValueError(f"Invalid variable definition: {line}")
                    self.labels[label] = address
                    address += 1
                    continue
                else:
                    # If there's no value, it's a label
                    label = parts[0].strip()
                    self.labels[label] = address
                    continue
            
            if line.split()[0].upper() in self.instructions:                                                                                            
                address += 1 + len(line.split()) - 1  # Instruction + operands
            else:
                raise ValueError(f"Unknown instruction or malformed line: {line}")

        # Second pass: generate machine code
        for line in lines:
            line = line.split(';')[0].strip()  # Remove comments
            if not line or line.endswith(':'):
                continue
            
            # already processed label-only lines
            if ':' in line and not any(op in line for op in self.instructions):
                continue
            
            parts = line.split()
            instr = parts[0].upper()
            operands = parts[1:]
            
            if instr not in self.instructions:
                raise ValueError(f"Unknown instruction: {instr}")
            
            machine_code.append(self.instructions[instr])
            
            for operand in operands:
                if operand.isdigit():
                    machine_code.append(int(operand))
                elif operand in self.labels:
                    machine_code.append(self.labels[operand])
                elif operand.startswith('0x'):
                    machine_code.append(int(operand, 16))
                elif operand.startswith('0b'):
                    machine_code.append(int(operand, 2))
                else:
                    raise ValueError(f"Unknown operand: {operand}")
        
        # add data section
        for var, val in self.variables.items():
            machine_code.append(val)
            self.labels[var] = len(machine_code) - 1
            
        return bytearray(machine_code)


if __name__ == "__main__":
    source_code = """
        ;calculate a + b
        LOAD a
        ADD b
        a:2
        b:3
    """
    asm = Assembler()
    program = asm.assemble(source_code)
    print("Assembled Machine Code:", list(program))
    print("Assembled Machine Code in binary:", [bin(x) for x in list(program)])
