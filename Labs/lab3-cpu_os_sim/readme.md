### 实验3：CPU/内存模拟与程序执行

*XSUN@GZHU
2026/11/08*

#### 实验目的
1. 理解CPU和内存运行的原理
2. 理解机器指令与汇编，理解程序执行的特点
3. 实现简单进程控制块和PCB和操作系统，为进程调度实验做准备

#### 实验内容

##### 1. CPU & Memory
```python
class CPU:
    def __init__(self):
       self.pc 
       self.memory
       self.register
```
CPU就是一个无情的 **加载指令，执行指令**的机器
```python
class CPU:
    def run(self):
        while True:
            self.fetch() # 加载指令
            self.execute() # 执行指令
    
    def fetch(self):
        pass
    
    def execute():
        pass
```

+ 程序指针 PC: Program Counter
  ```python
  class ProgramCounter:
    def __init__(self):
        self.value = 0
    def inc(self):
        self.value += 1
    def reset(self):
        self.value = 0
    def set_value(self, value):
        self.value = value
  ```
+ 寄存器Register：
  ```python
    self.registers = {
        'ACC': 0,  # 累加寄存器
        'FLAGS': 0, # 标志寄存器
    }
  ```
+ 内存：连续存储空间，Python 列表简单模拟（无堆栈结构，所以，无法实现函数调用）
  ```python
  # self -> CPU
  self.memory = [0] * self.memory_size
  ```
+ ALU(算数逻辑单元) $\to$ 指令集：自定义机器指令
  ```python
  # self -> CPU
  self.instruction_set = {
    0x01: self._load, # Load TO ACC
    0x02: self._add, # add ACC
    ...
  }

  def _load(self):
    addr = self.memory[self.pc.value]
    self.pc.inc()
    self.registers['ACC'] = self.memory[addr]

  def _add(self):
    addr = self.memory[self.pc.value]
    self.pc.inc()
    self.registers['ACC'] += self.memory[addr]
    ...
  ```

#### 2. 机器码和汇编器：Machine Language & Assembler
```asm
; calculate a+b
LOAD a
ADD b
a:2
b:3
```
上述汇编代码的运算结果需使得CPU的`ACC`寄存器：`ACC = 2 + 3 = 5`

1. 文本处理：去除空格和注释
2. 代码解析：区分标签label, 变量variables和指令
3. 根据指令生成机器码，内存地址转换

请参考[`asm.py`](./asm.py)中的是实现，并测试：
```py
# asm.py
source_code = """
;calculate a + b
LOAD a
ADD b
a:2
b:3
"""
program = asm.assemble(source_code)
print("Assembled Machine Code:", list(program))
print("Labels:", asm.labels)
print("Variables:", asm.variables)
```


#### 3. 简单OS模拟与进程控制块PCB
我们学习了操作系统对进程进行描述和控制是通过进程控制块完成的：
```py
class State(Enum):
    NEW = auto()
    READY = auto()
    RUNNING = auto()
    WAITING = auto()
    TERMINATED = auto()

class PCB:
    def __init__(self, pid, name, program):
        self.pid = pid # 进程标识符identity
        self.state = State.READY # 进程状态
        self.name = name # 进程名
        self.program = program # 进程的程序代码, 需要加载到内存中
```
OS负责创建进程，修改进程状态，加载程序至内存，控制CPU执行等：
```python
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
        pass
        self.ready_queue.append(PCB(self.next_pid, name, program))
        
    def load_program(self, process:PCB):
        # load the program into memory
        pass

    def run(self):
        pass
```

#### 实验要求
1. 在提供的`cpu.py`, `pyos.py`和`asm.py`的基础上进行开发，编写汇编代码实现斐波那契数的打印：
   - 修改`asm.py`文件：添加新的指令
   - 修改`cpu.py`文件：添加新的机器指令`xxx`并实现`self._xxx(self)`，需要和`asm.py`中的对应；在`pass`处实现方法对应的功能
   - 修改`pyos.py`文件：添加必要的代码，并在`pass`处实现方法对应的功能，最终在`pyos.py`中完成程序验证：
     ```py
       os = OperatingSystem()
       asm = Assembler()
       # 示例加法程序，source_code需要改成打印斐波那契数列的汇编程序
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
     ```
   - 提示：
     - 需要用到循环，所以要实现**跳转指令**，并注意使用程序计数器PC的`set(value)`方法实现指令的跳转执行。
     - 需要打印，可以设置一个简易的打印指令：`PRINT`，打印`ACC`中的值。（实际中打印到终端需要系统调用，这里只做简单模拟）

2. 验证与分析程序执行结果以及CPU的内存和寄存器状态的正确性。

#### 报告提交
前往 SUNJUDGE:https://judge.xuelongsun.cn 查看实验报告模板，具体提交要求，评分标准，参考代码和截止时间等，并按时提交实验报告。

注：实验讲义和SUNJUDGE系统都提供了框架代码文件：`cpu.py`,`asm.py`和`pyos.py`。
