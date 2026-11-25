### 实验5：连续内存分配
*XSUN@GZHU
2026/11/24*

#### 实验目的
1. 理解连续内存分配方式中的固定/动态内存分配的原理和相关算法
2. 通过模拟内存的分配**Allocate**和回收**Deallocate**的内部机制，加深对分时系统内存管理的理解

#### 实验内容
##### 1. 内存模拟
`memory.py`: 使用Python构建内存基类，在此基础上实现固定分区和动态分区内存：
```py
class Memory:
    def __init__(self, size=100):
        self.size = size # KB
        self.blocks = []
        
    def allocate(self, start, length):
        raise NotImplementedError("Allocate method not implemented")
    
    def deallocate(self, start, length):
        raise NotImplementedError("Deallocate method not implemented")
```
为了方便可视化内存分配效果，使用内存块`block`来表示内存分区/被进程占用的地方，`MemoryBlock`的实现：
```py
class MemoryBlock:
    def __init__(self, start, length):
        self.name = None
        self.start = start
        self.length = length
        self.free = True
    
    def mark_allocated(self, name):
        self.name = name
        self.free = False
```

##### 2. 固定分区分配
基于内存基类`Memory`,实现固定分区的内存分配方法：
```py
class FixedMemory(Memory):
    def __init__(self, size, block_size):
        super().__init__(size)
        self.block_size = block_size
        if isinstance(block_size, list):
            # 用户指定各固定分区的大小
            pass
        else:
            # 各分区一样大，则给定size后均分即可
            num_blocks = size // block_size
            ...
    def allocate(self, name, size):
        # 返回分配到的内存的起始地址
        ...
        return block.start
    
    def deallocate(self, start):
        # 回收起始地址为start的内存块block
        pass
```

+ 分区大小相同
```py
fixed_memory = FixedMemory(size=100, block_size=20)
```
+ 分区大小不同
```py
block_size=[5, 5, 5, 10, 10, 15, 15, 20, 25, 25, 30]
fixed_memory = FixedMemory(size=sum(block_size), block_size=block_size)
```

##### 3. 动态分区分配
同样基于内存基类`Memory`，初始化时有一个总的分区：
```py
class DynamicMemory(Memory):
    def __init__(self, size, policy="worst-fit"):
        super().__init__(size)
        # 有一个总的分区，之后被不断划分
        self.blocks.append(MemoryBlock(0, size))
        self.policy = policy
    
    def allocate(self, name, size):
        if self.policy == "first-fit":
            pass
        elif self.policy == "best-fit":
            pass
        elif self.policy == "worst-fit":
            pass
    
    def deallocate(self, start):
        # 回收起始地址为start的内存块block
        pass
        # 合并前后的空闲块：block.free == true
        ...
```
难点较固定分区在于：**内存回收时相邻的空闲区需要合并`block`。**

+ 首次适应
  ```py
  memory = DynamicMemory(size=100, policy='first-fit')
  ```
+ 最佳适应
  ```py
  memory = DynamicMemory(size=100, policy='best-fit')
  ```
+ 最坏适应
  ```py
  memory = DynamicMemory(size=100, policy='worst-fit')
  ```

##### 4. 测试与比较
在`run.py`中进行：
+ 随机生成进程序列：
  ```py
  def generate_requests(time_duration=[2, 10], size_range=[6, 25], prob=0.7):
    global requests # 保存生成的进程
    if random.random() > prob:
        return None
    time_d = random.randint(time_duration[0], time_duration[1])
    size = random.randint(size_range[0], size_range[1])
    request = {
        'name': f"P{len(requests)+1}",
        'time_duration': time_d,
        'size': size
    }
    return request
    ```
    + 运行时间`time_duration`: 2~10
    + 请求内存大小`size_range`:6~25KB
    + 每个时间点产生一个新进程的概率：0.7
    + **也可以自己定义进程：**
        ```py
        request = {'name': f'P{len(requests)+1}', 'time_duration': 5, 'size': 20}
        # 多个进程
        processes = [
            {'name': 'P0', 'time_duration': 5, 'size': 20},
            {'name': 'P1', 'time_duration': 2, 'size': 7},
        ]
        
        def run(memory:FixedMemory | DynamicMemory):
            global requests, clock, failed_num, processes
            request = processes[clock%len(process)]
            ...
        ```
+  可视化内存(已实现)：
   ```py
   def visualize_memory(memory:FixedMemory | DynamicMemory):
    # 可视化内存块
    # 红色 - 被占用，显示 进程名：块大小
    # 无色 - 空闲，只显示块大小
    # 显示的块长度和内存块大小成正比
   ```

+ 交互式运行：
  ```shell
  python3 run.py dynamic[fixed] first-fit[block_size]
  ```
  例如，固定分区大小，各分区大小为：5, 5, 5, 10, 10, 15, 20, 20:
  ```shell
  python3 run.py fixed 5,5,5,10,10,15,20,20
  ```
  动态分区大小，采用最坏适应：
  ```shell
  python3 run.py dynamic worst-fit
  ```
  运行后，`回车Enter`会模拟一个时间步长，`a` 会自动运行指定的时间，`q`会结束并显示内存申请失败的次数，`r`可以重置仿真。

#### 实验要求
+ 以`memory.py`中的代码为基础进行开发,运行`run.py`来测试结果。
+ 至少实现固定分区分配、动态分区中的FF, BF, NF 和 WF算法。
+ 实验报告中需要给出明确的验证证据来支持内存分配算法实现的正确性，并比较所实现的内存分配算法。
+ 附加实验，不作强制要求：
  + 尝试实现Quick Fit和Buddy System。
  + 除了已给出的`run.py`中已经计算的分配失败次数统计外，计算和比较各个算法的按时间变化的内存利用率。
> 注意：`run.py`是完全可运行的(需要额外的`colorama`包，可使用`pip install colorama`安装)，如果不做额外的实验，建议不要修改此文件。

#### 报告提交
前往 SUNJUDGE:https://judge.xuelongsun.cn 查看实验报告模板，具体提交要求，评分标准，参考代码和截止时间等，并按时提交实验报告。
