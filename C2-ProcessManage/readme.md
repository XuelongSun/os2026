## 第二章  进程管理
*XSUN@GZHU
2026/09/02*

---
上一章结尾我们从一个`hello_c`程序的运行看到了操作系统如何支持用户通过程序使用计算机的。事实上，如今运行在计算机上的各种应用，包括Word, Excel, 大型3D游戏，浏览器，Codex客户端等等，其本质不过只是一个比`hello_c`复杂一些的程序而已。

本章我们澄清究竟什么是程序，什么是进程(包括什么是线程)，然后观察分时操作系统如果要支持多程序的同时运行(并发-concurreny)，又要解决哪些问题，并理解这些问题时如何被解决的。

如此，我们便能理解操作系统进程管理中的诸多概念，不能死记硬背这些概念，而要从工程的角度理解他们出现的必然性！

### 程序-线程-进程
本章的标题是进程管理，那我们首先要明白什么是进程？

它是Windows任务管理器中显示的内容，还是Linux中`top`命令的输出？

要想理解什么是进程，我们首先要理解什么是程序？

#### 程序 Program
`hello.c` 和 `hello_c` 是程序吗？

- `hello.c` 是C语言代码文件，不是程序！
- `hello_c` 是程序!

程序本质是一个可执行文件，里面主要保存：CPU将来需要执行的机器指令、数据和一些运行配置信息。所以，程序本身不会“运行”，它只是磁盘上的一堆字节。

当我们执行(或者在Windows中双击`.exe`)：
```bash
./hello
```
时，一个程序才正在"运行"了起来！而所谓的运行起来：
- 从硬件角度看：CPU取指令执行指令的过程
- 从软件角度看：操作系统中的一个"运行世界"

《计算机组成原理》会让你深刻理解上面的硬件视角，而操作系统课程将从软件视角带你触碰这个程序的"运行世界"！

为了更清晰地看到这个"运行世界"，我们先从一个具体的例子深入地理解一下程序的运行现场。

##### 执行现场
对于如下C程序：
```c
int add(int x, int y)
{
    int z = x + y;
    return z;
}

int main()
{
    int a = 10;
    int b = 20;
    int c = add(a, b);
    int d = b - a;
    return 0;
}
```
调用`add()`前需要记录当前执行到的地址`addr`，调用完后需要让程序指针`PC(RIP)`再指向`addr`，从而回到`main()`调用前的位置继续执行。此外，除了返回地址，我们还要保存调用参数`a`和`b`，以及`main()`和`add()`的执行现场，其中包含着他们各自的局部变量，寄存器状态等。

那这些信息又是如何保存的呢？我们来看一个更复杂的例子：
```c
// source/concept/call.c
#include <stdio.h>

void B(void)
{
    int b = 20;
    printf("B: &b = %p\n", (void *)&b);
}

void A(void)
{
    int a = 10;
    printf("A: &a = %p\n", (void *)&a);
    B();
}

int main(void)
{
    int m = 0;
    printf("main: &m = %p\n", (void *)&m);
    A();
}
```
考察这个程序的调用和返回顺序，我们发现：
- 调用顺序：`main() – A() – B()`
- 返回顺序：`B() – A() – main()`

也就是说，最先调用的最后返回，具备"后入先出-Last In First Out"也就是LIFO的特性，这恰恰暗合了一种重要的计算机数据结构—— **栈(stack)** 的特点！因此，我们使用 **栈(stack)** 这种数据结构来保存函数调用和返回的现场！

栈的物理本质就是一片内存区域，只不过它遵循后入先出的准则，我们使用：
- `push`:向栈中存入一个数据
- `pop`:从栈中弹出一个数据
- `rsp`寄存器记录栈顶指针（栈顶的内存地址）

并且，x86规定栈向低地址增长，例如，初始化栈顶为`rsp=0x1000`：
```
rsp -> 0x1000 : 0x0000
```
执行：`push 0x10`, `push 0x55`后，栈变成：
```
       0x1000 : 0x00
       0x0fff : 0x10
rsp -> 0x0ffe : 0x55
```
再执行`pop ax`后，寄存器ax中的值为`0x55`，且栈变为：
```
       0x1000 : 0x00
rsp -> 0x0fff : 0x10
```

我们可以运行上述编译和运行上述程序，观察每个函数中的局部变量的内存地址：
```bash
gcc -O0 call.c -o call
./call
```
典型输出：
```
main: &m = 0x7ffed0f88134
A: &a = 0x7ffed0f88114
B: &b = 0x7ffed0f880f4
```
你会发现：`&m > &a > &b`，与我们的函数调用顺序一致！这也证明每进行一次函数调用，栈都会增长，因为存储在栈上的局部变量的地址在变小(栈向低地址增长)!

因为每一次函数调用的现场（调用参数，局部变量，寄存器，返回地址等）都保存在栈上，所以我们称之为一个"栈帧 stack frame"！

我们可以使用`gdb`([GNU Project Debugger](https://sourceware.org/gdb/))来查看调用栈（需要`gcc`保留栈帧信息）：
```
gcc -O0 -g -fno-omit-frame-pointer call.c -o call_frame
gdb ./call_frame
```
然后我们在`gdb`中可以看到函数的调用现场和栈帧：
```
break B
run
bt 
```
典型输出
```
#0  B () at call.c:4
#1  0x00005555555551ff in A () at call.c:13
#2  0x0000555555555258 in main () at call.c:20
```
还可以看寄存器和局部变量信息：
```
p $rsp
info registers rsp rax
info locals
```
由此，我们便看到：栈就是CPU在执行程序时保存函数调用现场的真实机制！

##### 执行流
那现在问个问题：
> 假设程序当前运行到 B()。那么要描述“这个程序现在执行到哪里”，最少要知道什么？

由上面的知识，我们明白要恢复`B()`的现场，我们要知道：
- PC / RIP：当前执行到哪条指令了？
- Registers: CPU寄存器的状态
- RSP：当前的栈在哪里？
- stack: 函数调用历史和局部状态

我们可以称以上现场信息为**执行流**：一套可以独立继续执行下去的 CPU 状态。

现在想象一个复杂一些的程序（应用），一个聊天软件：
```c
while (1) {
    等待用户输入;
    接收网络消息;
    刷新界面;
    保存文件;
}
```
这个应用一定不能因为一直等待用户输入，就卡住！所以，自然的想法是：
```
执行流 1：处理界面
执行流 2：接收网络
执行流 3：保存文件
```
也就是：一个运行中的程序，希望存在多个可以独立推进的**执行流**。操作系统把这种执行流抽象成一个概念：**线程（Thread）**。

#### 线程Thread
有了线程的概念，我们就可以把聊天应用抽象成一个多线程应用：
```c
// global vars;
// global files;
int main()
{
    while(1)
    {
        thread1("处理用户输入");
        thread2("界面渲染");
        thread3("处理用户输入");
        thread4("文件处理");
    }
}
```
每个线程都是一个独立执行流，所以每个线程都需要有：PC/RIP, 寄存器，RSP和stack, 但是它们都处于同一个程序中，所以，可以共享：
- 程序代码
- 已初始化的全局数据
- 打开的文件
- 堆Heap (存储程序运行之后的动态数据)

所以，这个多线程程序的模型可以表示为：
```
┌───────────────────────────┐
│            Code           │
├───────────────────────────┤
│        Global Data        │
├───────────────────────────┤
│            Heap           │
├───────────────────────────┤
│ Stack 1        Stack 2    │
│   ↓              ↓        │
│ Thread 1       Thread 2   │
│ PC/Regs        PC/Regs    │
└───────────────────────────┘
```
我们可以用一个多线程示例来看，线程之间共享了什么，而什么是独立的：
```c
// source/concept/thread.c
#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include <unistd.h>

int global = 100;
int *heap;

void *worker(void* arg)
{
    int local = 0;
    printf("Thread:\n");
    printf("  &global = %p\n", (void *)&global);
    printf("  heap    = %p\n", (void *)heap);
    printf("  &local  = %p\n", (void *)&local);
    return NULL;
}

int main(void)
{
    pthread_t t1, t2;
    heap = malloc(sizeof(int));
    pthread_create(&t1, NULL, worker, NULL);
    pthread_create(&t2, NULL, worker, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    free(heap);
    return 0;
}
```
编译运行：
```bash
gcc -O0 -g thread.c -o thread -pthread
./thread
```
典型输出：
```
Thread:
  &global = 0x5677113eb010
  heap    = 0x567723aea2a0
  &local  = 0x75b35d5fde44
Thread:
  &global = 0x5677113eb010
  heap    = 0x567723aea2a0
  &local  = 0x75b35ddfee4
```
你会发现，每个线程的`local`是存在自己的栈帧上的，所以地址不同，而global和heap是共享的。

而这个让他们共享这些数据和资源的实体，也就是我们开头提到的"运行世界"，就是**进程Process**！

#### 进程 Process
线程之间可以共享全局数据，因为它们本质上存在于进程之中。

那进程之间可以共享数据吗？因为它们存在于同一个OS之中？

简单思考一下，也知道，进程之间必须隔离。不然你在Offic Word中就可以操作浏览器了:smile: ！并且，进程隔离可以保证：一个进程出错了，不会影响其他进行，更不会影响你的计算机。

> 所以，操作系统一定要让进程之间隔离。

为了演示，我们在Linux中运行下面的程序：
```c
// source/concept/isolate.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int x = 0;
int main(int argc, char *argv[])
{
    if (argc != 2) {
        printf("usage: %s number\n", argv[0]);
        return 1;
    }
    x = atoi(argv[1]);
    
    while (1) {
        printf("x=%d\n",x);
        sleep(2);
    }
}
```
我们可以运行多个上述程序：
```
gcc isolate.c -o isolate
./isolate 1111
```
然后另一个终端运行：
```
./isolate 2222
```
两个程序运行，发现变量`x`的值是不同的。

在操作系统的加持下：运行的是同一个程序，却产生了相互独立的不同进程。这再一次体现出了程序只是静态的文件，而进程是动态的"运行世界"！而这个运行世界，包含了如下内容：

- 程序代码
- 数据
- 堆
- 打开的文件
- 若干线程
  - registers
  - rip
  - rsp
  - stack
- ...

这便是"进程"在操作系统里真正样子(的一部分)！因为后面还有省略号，随着我们学习的深入，这些省略号也会慢慢有具体的内容！敬请期待~ :grin:

好了，到这里，我们总结一下：

| 概念      | 最核心的问题      | 本质      |
| ------- | ----------- | ------- |
| Program | 要执行什么？      | 静态代码与数据 |
| Process | 资源属于谁？和谁隔离？ | 资源与隔离容器 |
| Thread  | 谁在执行？       | CPU执行流  |

所以：
> Program  = 要执行的代码
> Process  = 程序运行所处的资源与隔离环境
> Thread   = 这个环境中真正向前执行的执行流

它们的关系，也可以总结为下图：

![](./figures/program-thread-process.png)


### 并发 Concurrency
理解了进程之后，我们知道，分时操作系统允许用户“同时”运行多个进程，这个打印好的同时，就是并发Concurrency。

> PS: 并发Concurrency和并行parallelism 是有区别的。并行，才是真正意义上的"同时发生"(多核系统)，而并发，只是看起来像是同时发生，实际上CPU在每个时刻只能执行某个进程的指令。

我们甚至可以从同一个程序来产生不同的进程，比如我们之前测试所用的`./isolate`：
```
./isolate 1111 &
./isolate 2222 &
```
在Linux系统中，我们可以用`ps`命令来获得进程信息：
```
ps aux | grep isolate
```
典型输出：
```
sxl   345460  268960  0 22:04 pts/6    00:00:00 ./isolate 2222
sxl   345501  343149  0 22:04 pts/7    00:00:00 ./isolate 1111
```
我们之前讲过，这两个进程是完全独立的，它们都不知道彼此的存在。我们来修改一下程序，进一步体会这种独立性：
```c
// source/concept/isolate_memory.c
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
int x = 0;
int main(int argc, char *argv[])
{
    if (argc != 2) {
        printf("usage: %s number\n", argv[0]);
        return 1;
    }
    x = atoi(argv[1]);
    printf("&x  = %p\n", (void *)&x);
    while (1) {
        printf("x=%d\n",x);
        sleep(2);
    }
}
```
其实这个代码之比，`isolate.c`多了一句话：
```c
printf("&x  = %p\n", (void *)&x);
```
就是打印变量`x`的地址。

同样使用`gcc`编译，但是注意要加上`-fno-pie`参数让其不要生成位置无关可执行文件所需的代码, `-no-pie`在链接阶段不要生成那种可以被 Linux 动态加载器随机放置的可执行文件：
```
gcc -O0 -fno-pie -no-pie isolate_memory.c -o isolate_memory
```
运行发现，两个程序`x`的地址完全一样！

看着不合理，实际上这个地址是虚拟地址，不是真正的内存物理地址！这里先埋个伏笔，我们在内存管理再来打开它！

由上面的实验可以发现：OS中多进程是完全隔离的，这保证了系统的安全！但如果进程之间真的想要**合作**怎么办？比如：
```bash
cat data.txt | grep error
```
`cat`和`grep`是不同的进程，但是我们却需要他们之间合作完成一个更复杂的任务。这就涉及到操作系统中一个很重要的问题——**IPC: Inter-Process Communication**：操作系统如何为进程间的合作提供支持？

### IPC
Linux为进程间的合作提供了多种方式：
1. pipe
2. shared memory
3. message queue
4. signal
5. ...

本质上可以分成两大类：**通信 Message passing**与**共享内存 shared memory**。我们刚才用到的：
```bash
ps aux | grep
```
就属于进程**通信**中的**管道pipe**，它的实现示意：
```
 ps                           grep
 │                             ⭡
 │ write                       │ read
 ↓                             │
┌───────────────────────────────────┐
│             Pipe                  │
└───────────────────────────────────┘
```
因此，IPC机制为本来相互隔离的进程，提供了“合法穿过隔离边界”的通道。我们可以使用python非常方便使用OS为我们提供的管道功能：
```py
import os
r, w = os.pipe()
pid = os.fork() # 创建一个子进程
if pid > 0:
    os.close(r)
    os.write(w, b"Hello from parent!") # 父进程写
    os.close(w)
else:
    os.close(w)
    data = os.read(r, 100) # 子进程读
    print(f"Child received: {data.decode()}") 
    os.close(r)
```
> 注：上述程序只能在Unix上执行，Windows上没有`fork()`系统调用，运行会报错。

这体现了操作系统的设计哲学：

> 默认隔离，显式合作。也就是：受保护的独立性 + 受控制的合作。

那么，对于**共享内存**的这种合作方式呢？比如进程A和进程B都要更新一个变量`counter=100`：
```c
counter = counter + 1
```
能否保证最后`counter=102`？我们来验证一下这个问题。如何验证呢？

事实上，我们可以使用`mmap`这个系统调用来实现共享内存，但是过于复杂。其实，我们有一个天然合适的平台来实验这种共享变量的同时更新问题！没错，就是线程！因为，线程共享全局变量！我们来写一个这样的多线程程序：
```c
// source/mutual_exclusion/sum.c
#include<stdio.h>
#include<pthread.h>

#define N 1000000
long sum = 0;

void *Tsum(void *arg) {
    for (int i = 0; i < N; i++){
        sum++;
    }
}

int main(){
    pthread_t tA, tB;
    pthread_create(&tA, NULL, Tsum, &sum);
    pthread_create(&tB, NULL, Tsum, &sum);
    pthread_join(tA, NULL);
    pthread_join(tB, NULL);
    printf("sum is %ld\n", sum);
}
```
编译和运行上述程序（运行10次），
```bash
seq 10 | xagrs -I {} ./sum
```
会发现`sum`的值不是期待的`2,000,000`，而是比其要小，这是为什么？

因为`sum`被两个线程“同时”读写，会发生：
| 时刻 | Thread A      | Thread B      | sum |
| -- | ------------- | ------------- | --: |
| 1  | load sum → 10 |               |  10 |
| 2  |               | load sum → 10 |  10 |
| 3  | add → 11      |               |  10 |
| 4  |               | add → 11      |  10 |
| 5  | store 11      |               |  11 |
| 6  |               | store 11      |  11 |

看上去加了2次，实际上`sum=11`。这就是当不同线程(甚至进程)共享
同一个数据时，会发生:**竞争条件(race condition)**，结果依赖于**不可预测的执行交错**。

为了保证一组操作执行时不被其他线程并发执行，我们把这段代码称为 **critical section（临界区）**。把被临界区访问的数据（内存）叫做**临界资源Critical Resource**。临界区就是操作系统为了让进程正确地共享临界资源需要真正关心的地方！

那么，如何实现正确地访问临界资源呢？这需要OS保证不同临界区能够**互斥mutual exclusion** 地访问临界资源！

### 互斥-Mutual Exclusion
如何实现互斥，已让`sum.c`正确输出`2000000`呢？朴素的想法是，线程A读写临界资源`sum`时，把它锁上，访问完了再把锁打开：
```c
int locked = false;

void *Tsum(void *arg) {
    for (int i = 0; i < N; i++){
        while (locked); //wait
        locked = true; //上锁🔒
        sum ++;
        locked = false; //解锁🔓
    }
}
```
我们试一试这样可行吗, 运行发现失败了，这是为什么呢？

因为全局变量`locked`也说临界资源，我们也无法保证其读写不被打断。如果：
```c
while(locked); 
locked = true; 
```
这两句需要一起完成，不能被打断，都在进程A,B可能都会跳过`while`循环。这种不能被打断(without interruption)的操作，我们称之为"**原子操作atomic operation**"。

想要保证操作是原子的，很困难，它需要硬件的支持(后面会说)，但是我们先从软件上看看有没有更好的方法来实现互斥呢？

#### Peterson 算法
这个算法的思想是针对A, B两个进程：
```
A：我要进临界资源(flag A)，但如果冲突让 B 先(turn = B)
B：我要进临界资源(flag A)，但如果冲突让 A 先(turn = A)
```
所以针对A的等待条件就是：
```c
while(flag B && turn==B);
```
因此，最后采写`turn`的进程，让出了优先权。实现的peterson算法见：[sum_peterson.c](./source/mutual_exclusion/sum_peterson.c)。我们运行一下，发现仍然没有得到我们想要的`2,000,000`! 

这说明Peterson算法是错的吗？不是，从C语言的逻辑语义上是正确的:

> Peterson 在它的计算模型里是正确的；但是普通 C 程序没有满足它依赖的计算模型。参加Peterson 1981年的[论文](https://zoo.cs.yale.edu/classes/cs323/doc/Peterson.pdf)~

Peterson 隐含两个非常重要的假设：
1. 对 `flag` 和 `turn` 的读写是原子的，不可分割！
2. 所有处理器看到的读写顺序与程序写出的顺序一致(循序一致性Sequential Consistency)，程序语义先后关系的保持！

但是现代计算机系统可能会改变上面两个假设：
1. 编译器优化可能重排顺序
2. 多核操作系统，看到的执行顺序很难保证一致

因此，Peterson算法为我们提供了基于协议的软件实现互斥的思想，但想要真正落地，还是需要硬件的支持！

#### 硬件原语 Hardware Primitives
这种把多个操作(读-改-写)变成一个不可打断的操作的硬件指令称为**硬件原语**。有了这个，实现互斥就变得简单有效很多。

最简单的解决互斥问题的硬件原语是**关中断**：

```c
void process(void *arg) {
    disable_interrupts();
    critical_section();
    enable_interrupts();
}
```

> 中断Interrupt: 是指可以让CPU暂时结束当前执行的程序去处理另一个更高优先级的事件的信号。中断非常重要，它使得CPU不再轮询检查设备，而是运行设备准备好时主动通知CPU，它是实现CPU多任务和实时控制的基础机制！

这样关闭中断功能后，CPU不会被中断，无法打断当前的任何操作，便实现了互斥。但这个方法：
1. 无法在多核系统上使用，别的CPU会介入执行
2. 即使在单核系统上也代价很大，若临界区过长，甚至影响计算机的功能，因为中断是很多重要功能，包括OS正常运行的基础。


TAS(Test-And-Set)是另一个重要的硬件原语：
```c
bool lock = false;

bool TAS(int *lock) {
    bool old = *lock;
    *lock = true;
    return old;
}
{
    while (TAS(lock));
    critical_section();
    lock = false;
} 
```
有了这个就可以保证我们之前的`sum_lock.c`可以正确地实现互斥。

但是，有了另外一个问题，如何在C语言中告诉编译器，对`lock`的检查和修改是原子的呢？

我们可以使用C11之后支持的`stdatomic.h`这个标准库来改写我们的锁：
```c
#include<stdatomic.h>

atomic_flag LOCK = ATOMIC_FLAG_INIT;

void lock(void)
{
    while (atomic_flag_test_and_set_explicit(
               &LOCK, memory_order_acquire));
}

void unlock(void)
{
    atomic_flag_clear_explicit(
        &LOCK, memory_order_release);
}
```

> 注意: C11 引入了标准原子操作, 编译器再根据 CPU 架构生成合适的原子机器指令。它是程序员、编译器和 CPU 之间关于并发语义的一份契约。并不一定意味着硬件架构中真有`test-and-set`等硬件指令。

我们将上述代码加入到之前的`sum_lock.c`中形成新的[sum_atomic_lock.c](./source/mutual_exclusion/sum_atomic_lock.c)，编译运行：

```bash
gcc -std=c11 sum_atomic_lock.c -o sum_atomic_lock -lpthread
./sum_atomic_lock
```

发现结果是我们期待已久的`2,000,000`了 :sunglasses: :balloon:！


此外，还有一种硬件原语：`swap`，又称`xchg`，可以原子地交换两个数的值，其来实现互斥的基本思想为：
```c
bool lock = false;
void swap(bool *a, bool *b) {
    bool temp = *a;
    *a = *b;
    *b = temp;
}
{   
    bool key = true;
    do {
      swap(&lock, &key)
    }while(key);
    critical_section();
    lock = false;
} 
```
可以这样理解：临界区前放着一把钥匙`key`，想要进去的人需要拿自己手中的锁去换钥匙，如果换到的确实是钥匙`key = true`，那就可以进去，否则说明钥匙被别人先换走了！

同样的，我们可以在C11的支持下来通过`exchange`来实现我们的互斥：
```c
#include <stdatomic.h>
atomic_bool locked = ATOMIC_VAR_INIT(false);

void lock(void)
{
    while (atomic_exchange_explicit(
               &locked,
               true,
               memory_order_acquire)) {
        ;
    }
}

void unlock(void)
{
    atomic_store_explicit(
        &locked,
        false,
        memory_order_release);
}
```
将上面的代码融入`sum.c`形成使用`swap(xchg)`来实现互斥:[sum_atomic_swap.c](./source/mutual_exclusion/sum_atomic_swap.c)。运行结果同样是`2,000,000`！

仔细分析我们的互斥程序，请问：当某个线程拿不到进入临界资源的权限时，它的动作是什么？

没错，就是一直检查是否可进入，因此我们上面实现的锁可被形象地称之为**自旋锁Spinlock**。

#### 自旋锁-Spinlock

我们已验证自旋锁可以实现互斥，但如果拿不到钥匙，会一直check某个资源是否可用，不做任何其他事情。这种动作，我们称之为CPU的“**忙等 busy waiting**”。CPU一直忙等且等待时间很久，是很浪费计算资源的。为此，我们需要重新定义拿不到访问临界资源钥匙的进程的动作，以提高CPU的利用率。

#### 互斥锁-Mutex

互斥锁就是为了解决CPU忙等而设计的锁，它的核心思想是，如果进程拿不到进入权限，不是忙等，还是进程被CPU阻塞进入睡眠状态，等到有钥匙了，再唤醒改进程：
```c
void syscall(int flag, _t* lk){
    if (flag == SYSCALL_lock){
        if (*lk){
            // state := blocked/sleeping
            sleep(); 
        }
        else{
            // state := ready
            *lk = true;
        }
    }
    if(flag == SYSCALL_unlock){
        *lk = false;
    }}
{   
    syscall(SYSCALL_lock, &lk);
    critical_section();
    syscall(SYSCALL_unlock, &lk);
} 
```
你可以看到，这里涉及到了系统调用，因为让一个进程睡眠已经超出了互斥这个议题，涉及到了操作系统的进程调度问题，我们会在下一章介绍，这里大家知道mutex解决忙等的基本思想即可，并且明白：
>spinlock 与 mutex 的核心互斥机制可以完全一样；真正不同的是失败后的等待方式。
但是，请问：

> 阻塞进程就一定比忙等好嘛？

不一定，要看情况，因为进程切换有开销！所以，等得不久就可以忙等，反而划算！所以，有了[Futex](https://jyywiki.cn/pages/OS/manuals/futexes-are-tricky.pdf)! (感兴趣的可以去了解，比较复杂)

虽然我们很难去实现一个mutex, 但我们仍然可以演示mutex的行为。

想想我们这里不是在用线程来讲进程并发的共享内存嘛，而C语言的线程库，是提供了用于线程的互斥锁的：
```c
// source/mutual_exclusion/sum_thread_mutex.c
#include<stdio.h>
#include<pthread.h>

#define N 1000000
long sum = 0;

pthread_mutex_t lock = PTHREAD_MUTEX_INITIALIZER;

void *Tsum(void *arg) {
    for (int i = 0; i < N; i++){
        pthread_mutex_lock(&lock);
        sum++;
        pthread_mutex_unlock(&lock);
    }
}

int main(){
    pthread_t tA, tB;
    pthread_create(&tA, NULL, Tsum, &sum);
    pthread_create(&tB, NULL, Tsum, &sum);
    pthread_join(tA, NULL);
    pthread_join(tB, NULL);
    printf("sum is %ld\n", sum);
}
```
这个程序的运行结果是`sum is 2,000,000`!而这个程序只比`sum.c`多了三行！

但是，你知道这三行并不简单，它的背后是竞争条件、原子操作、硬件原语、进程调度......等等。所以，学习操作系统，是体会计算机世界的奥妙。**学习进程并发，可以从根本上提升大家并发编程的能力！**

### 同步-Synchronization
通过上一节互斥的学时，我们明白，互斥的作用是解决多个线程同时操作全局变量(或多个进程操作共享内存-shared memory)。但，这不是并发带来的唯一问题，比如，A进程往一个buffer里写数据，B进程从这个buffer里读数据：

```
A --write-> [buffer] --read-> B
```
虽然A和B能够互斥地读写临界资源buffer以保证B读到的是A最新写的内容。但是：

- 如果A还没有写，B就从buffer读，会什么都读不到
- 如果A一直写，写满了buffer，B还没读，就会使得A无法再写入数据(或最早写的数据丢失)。

这当然不是我们所希望的！仔细思考：这2个问题产生的根本原因，是**A和B的执行顺序不合理**导致的！换句话说：

- 当buffer中没有数据的时候，B需要等待A写入后再读
- 当buffer数据满了的时候，A需要等B读取了之后再往里写

所以，A和B存在“等待另一方执行”的时候，这就是并发带来**同步Synchronization**问题。

上面这个读写buffer的例子非常经典，因此有个名字：**生产者-消费者问题**。写入数据的A进程是生产者，读取数据的B进程是消费者。很多的进程同步问题，都可以转化为生产者-消费者问题，比如，如何通过多线程实现合法的括号打印：
```c
{} // ✓
{{} // x
{{{{}} // x
{{}} // ✓
{{{{{{{{{{{}}}}}}}}}}}{}} // ?
```
人为判断太困难，我们可以写个程序来判断，python实现在:[checker.py](source/synchronization/checker.py)。

至于用来打印括号的多线程程序：我们可以让Producer打印**左括号**，让消费者打印**右括号**，相当于把左括号消费掉以完成括号的闭合：
```c
void* producer(void *args)
{
    while(1)
    {
        printf("{");
    }
}
void* consumer(void *args)
{
    while(1)
    {
        printf("}");
    }
}
```
如果我们不加任何的机制，直接执行(完整文件：[producer_consumer.c](source/synchronization/producer_consumer.c))：
```shell
./producer_consumer 2 2 4 | head -c 100 # 截取100字节
timeout --signal=SIGTERM 0.1s ./pro_con.o 2 2 4 # 运行0.1s
```
也可以直接送入python实现的checker检查：
```shell
./producer_consumer 2 2 4 | python3 checker.py 4
```
你会发现，很难正确！因此，问题的关键是，如何在多线程并发执行时保证输出的合法性？该如何解决生产者-消费者这个并发同步问题？

#### 互斥锁Mutex解决同步问题
我们能否用解决互斥的方法来解决这个生产者消费者问题呢？

#### 条件变量
#### 信号量
