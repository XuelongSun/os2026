### 实验2：进程的互斥与同步

*XSUN@GZHU
2026/10/29*

#### 实验目的:
1. 理解多进程并发中同步与互斥的重要性，及其实现方式，
2. 提高并发编程的能力。

#### 实验内容
通过不同方式实现有限缓冲区并用多线程进行测试，并用指标评价程序性能。

##### 有限缓冲区-BoundedBuffer
1. 用python实现一个boundedBuffer类，需要具有以下的功能：
```python
class BoundedBuffer:
    def __init__(self, capacity):
        self.capacity = capacity
        pass
    
    def put(self, item):
        pass

    def get(self):
        pass
```
+ 缓冲区大小：`capacity`
+ `put`操作：当缓冲区不满时，向缓冲区存入数据
+ `get`操作：当缓冲区非空时，从缓冲区读走数据

2. 错误的实现，没有任何互斥与同步机制的保证：
```python
class BoundedBuffer:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.buffer: List[Any] = []
        
    def put(self, item: Any):
        self.buffer.append(item)

    def get(self) -> Any:
        item = self.buffer.pop(0)
        return item
```
3. 不一定正确, 但是一定低效的实现:
   + 使用`count`变量: `put`就+1,`get`就-1,然后每次访问判断`count`是否满足某个条件.

4. 正确的实现方式
   + 使用1个锁 + 2个条件变量:`threading.Lock`,`threading.Condition`
   + 使用1个锁 + 1个条件变量
   + 使用信号量:`threading.Semaphore`

##### 多线程
多线程共享全局变量所需要解决的问题，和多进程通过共享内存进行合作所面临的问题的本质是一致的。本实验使用多线程编程来模拟进程并发中的互斥与同步问题。

+ 创建多个生产者（执行`put`）和消费者（执行`get`）线程.
+ 可以指定生产和消费的数据数量，比较不同实现方式的效率.
```python
bb = BoundedBuffer(5)
produced = []
consumed = []

def producer(i):
    while len(produced) < N:
        x = (i, random.randint(1,100))
        bb.put(x); produced.append(x)

def consumer():
    while len(consumed) < N:
        x = bb.get(); consumed.append(x)

threads = []
for i in range(n):
    threads.append(Thread(target=producer, args=(i,)))
    threads.append(Thread(target=consumer, args=(i,)))
```
+ 可以使用断言语句`assert`检测结果是否正确:
```python
assert len(consumed) <= len(produced)
print("Produced:", len(produced), "Consumed:", len(consumed))
```
##### 程序性能的评价
对于正确的实现，可用如下指标对程序性能进行评价：
+ 使用固定的生产/消费 `item` 的数量 $N$ ，计算程序运行时间 $t$ .
+ 使用`Throughput`吞吐量 $TP$ ：单位时间生产/消费`item`的个数.
  $$TP = \frac{N}{t}$$

#### 实验要求
1. 分别实现没有同步与互斥机制的保证、条件变量、信号量三种有限缓冲区。
2. 讨论缓冲区大小对程序性能的影响。
3. 选做：比较不同实现方式的性能差异。

#### 报告提交
前往 SUNJUDGE:https://judge.xuelongsun.cn 查看实验报告模板，具体提交要求，评分标准，参考代码和截止时间等，并按时提交实验报告。
