from cpu import CPU
from asm import Assembler
from enum import Enum, auto

class State(Enum):
    NEW = auto()
    READY = auto()
    RUNNING = auto()
    WAITING = auto()
    TERMINATED = auto()

class PCB:
    def __init__(self, pid, name, program):
        self.pid = pid
        self.state = State.READY
        self.name = name
        self.program = program
    
class OperatingSystem:
    def __init__(self):
        self.cpu = CPU()
        self.process = []
        self.next_pid = 1
        self.ready_queue = []
        self.clock = 0
        
    def create_process(self, program, name="Process"):
        # create a new process and add to the process list
        # like linux's fork()
        self.ready_queue.append(PCB(self.next_pid, name, program))
        pass
    
    def load_program(self, process:PCB):
        # load the program into memory
        pass
    
    def run(self, max_cycles=100):
        current_process = self.ready_queue.pop(0)
        current_process.state = State.RUNNING
        print(f"Running Process {current_process.pid} - {current_process.name}")
        self.load_program(current_process)
        while self.clock < max_cycles:
            self.cpu.run_step()
            self.clock += 1
            current_process.state = State.TERMINATED
        print(f"Process {current_process.pid} - {current_process.name} terminated.")

if __name__ == "__main__":
    os = OperatingSystem()
    asm = Assembler()
    source_code = """
        ;calculate a + b
        LOAD a
        ADD b
        a:2
        b:3
    """
    program = asm.assemble(source_code)
    os.create_process(program, name="Addition Program")
    os.run(max_cycles=2)
    print("Final CPU State:")
    os.cpu.dump_registers()
    os.cpu.dump_memory(0, 16)
