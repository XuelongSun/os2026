### 实验4：进程调度

*XSUN@GZHU
2026/11/16*

#### 实验目的
1. 理解作业与进程调度算法的原理
2. 理解进程切换需要做的相关工作
3. 通过在[实验3](../lab3-cpu_os_sim/readme.md)所设计的CPU上完成进程调度，进一步理解进程调度与进程切换开销

#### 实验内容
#####  1. 进程调度

+ 非抢占式((non-preemptive))作业调度
  + 先来先服务 FCFS
  + 短作业优先 SJF
+ 抢占式(preemptive)作业调度算法：
  + RTF(shortest remaining time first)
+ 进程调度
  + 高响应比优先：HRRN-Highest Response Ration Next
  + 基于优先级的调度算法：priority based scheduling algorithm
  + 轮转调度 RR-round robin
  + windows：多级反馈队列 MLFQ-multi-level feedback queue
  + Linux: 完全公平调度 CFS-completely fair scheduler

##### 2. 程序实现 
进程调度是在OS中完成的，所以需要修改[实验3](../lab3/readme.md)中的`pyos.py`中的`OperatingSystem`类:

+ 增加调度函数：
  ```py
    def schedule(self, policy="RR"):
        if policy == "RR":
            pass
        elif policy == "SRTF":
            pass
        elif policy == ""
  ```
+ 增加保存和恢复现场，以及切换进程的函数：
  ```py
  def save_cpu_context(self):
      pass

  def load_cpu_context(self, context):
      pass

  def switch_process(self, current_process:PCB, next_process:PCB):
      pass
  ```
+ 修改运行函数在每个CPU时钟上重建就绪队列并执行调度算法：
  ```py
  def run(self, max_cycles=100):
    # 初始化与准备
    # ...
    while self.running and cycles < max_cycles:
        # 执行主体
        # ...
        self.clock += 1
  ```

进程的现场数据需要保存在PCB中，所涉及的算法需要知道进程的其他相关信息，比如到达时间，运行时间等，因此还需要修改`pyos.py`中的`PCB`类
```py
class PCB:
    def __init__(self, pid, name, time, program, start_addr=0):
        self.pid = pid
        self.state = State.READY
        self.name = name
        self.program = program

        # 添加新的属性以实现进程正确的切换
        # ...
```
#### 实验要求
+ 至少实现两种课上所教的可抢占式进程调度算法(多实现多加分:smile:~)，并跑通测试。验证时可以提供不同的`source_code`，如：
  ```py
  if __name__ == "__main__":
    os = OperatingSystem()
    asm = Assembler()
    source_code1 = """
        ;calculate a + b
        LOAD a
        ADD b
        a:2
        b:3
    """
    source_code2 = """
        ;calculate a - b
        LOAD a
        SUB b
        a:5
        b:7
    """
    program1 = asm.assemble(source_code1)
    program2 = asm.assemble(source_code2)
    os.create_process(program1, name="Addition")
    os.create_process(program2, name="Subtraction")
  ```
  > 注意：这只是简单示例，为了更清楚地看到调度效果，程序需要有一定的长度，需要消耗一定的CPU时间, 比如可复用实验3的斐波那契数列的程序。
+ 本实验的框架代码基于[实验3的`pyos.py`](../lab3-cpu_os_sim/pyos.py)，请在[实验3](../lab3-cpu_os_sim/readme.md)的基础上完成。
+ 完成实验报告，要求列出输出证据并作说明，具体参考实验报告模板。


#### 报告提交
前往 SUNJUDGE:https://judge.xuelongsun.cn 查看实验报告模板，具体提交要求，评分标准，参考代码和截止时间等，并按时提交实验报告。

