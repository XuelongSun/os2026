class ProgramCounter:
    def __init__(self):
        self.value = 0

    def inc(self):
        # increment the program counter
        pass
    
    def set(self, value):
        # set the program counter to value
        pass
    
    def reset(self):
        # reset the program counter to 0
        pass

class CPU:
    def __init__(self):
        # initialize registers, memory, program counter, etc.
        pass
        # instructions set should match the assembler
        self.instruction_set = {
            0x01:self._load, # Load TO ACC
            0x02:self._add, # add ACC
        }
    
    def run(self):
        while True:
            self.fetch() # 加载指令
            self.execute() # 执行指令
    
    def fetch(self):
        pass
    
    def execute(self):
        pass
    
    def run_step(self):
        # run a single instruction
        # for OS use
        self.fetch() # 加载指令
        self.execute() # 执行指令
    
    def dump_registers(self):
        # print the register values
        pass
    
    def dump_memory(self, start=0, end=16):
        # print the memory values from start to end
        pass
    
    # implement CPU instructions
    def _load(self, address):
        # load value from memory to ACC
        pass
    
    def _add(self, address):
        # add value from memory to ACC
        pass
