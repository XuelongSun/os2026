### 实验1：操作系统接口

*XSUN@GZHU
2026/10/20*

#### 实验目的
1. 体验操作系统提供的三种接口(Interface):
   - 命令行Command Line Interfacce-CLI
   - 图形界面GUI-Grapical User Interface
   - 系统调用System Call

2. 思考每种接口的最佳使用场景
3. 了解以Linux为内核的操作系统的基本使用

#### 实验准备
Linux是一个优秀的免费、开源的类 Unix 操作系统。作为信计的学生是有必要了解的。

其主要组成部分：
1. Linux 内核：负责管理 CPU、内存、存储及硬件设备通信的最底层核心。
2. 发行版（Distribution）：由内核加上图形界面（如 X Window）、桌面环境、包管理工具以及各类应用软件组合而成的完整操作系统。常见[发行版](https://www.kernel.org/)：
   - Ubuntu / Debian：以出色的稳定性和庞大的软件仓库著称，适合桌面与服务器。
   - Red Hat Enterprise Linux (RHEL) / CentOS Stream / Rocky Linux：企业级应用最广泛的发行版之一。
   - Linux Mint：主打开箱即用、低维护成本的个人桌面系统。

##### Linux环境
我们需要一个Linux环境，从而方便我们体验命令行接口，**现在的AI-Agent几乎都是通过命令行接口来完成用户的协助请求的**，所以，这是非常有价值的需要学习和了解的内容。

1. 如果你已有Linux系统，则无需额外准备
2. 如果你是Windows：
   + (1) 安装wsl：Windows Subsystem Linux:
        > 需要 Win11，其他版本(x64 系统：版本 1903 或更高版本，内部版本为 18362.1049 或更高版本), 请参阅：[手动安装wsl](https://learn.microsoft.com/zh-cn/windows/wsl/install-manual)
       
       以下命令只对win11有效：
       + 以管理员身份打开命令行cmd:
        ```
        wsl.exe --list --online
        ```
        查看可安装的发行版distro,使用如下命令安装对应的发行版
         ```
         wsl --install [distro]
         ```
         如：
         ```
         wsl --install Ubuntu-20.04
         ```
       + 有问题可以尝试：控制面板->程序->启用/关闭Windows功能->勾选`适用于Linux的Windows子系统` 和 `Hype-V`.
  
    + (2) 通过VMWare/VirtualBox 安装Linux虚拟机
    > 推荐使用wsl，因为可以和windows进行跨系统文件访问，非常方便

3. 如果你是MacOS: MacOS也是unix-like的，所以依然可以完成实验。具体操作的话， unfortunately, you should check what you can do and what you can not!

Linux环境准备好后，在你的用户文件夹下`/home/username`创建一个目录(文件夹)：`/osLabs`，用于存放我们实验的文件。

##### 编辑器
1. Install `VSCode` with `python` and `markdown` extensions (`Markdown Preview Enhanced`,`Markdown All in One`,`Markdown PDF`).
2. `Vim` (+ plugins) is also good if you can use it efficiently.
3. 实验报告使用Markdown编写，quick start: [Markdown](https://www.markdownguide.org/cheat-sheet/) 

##### Linux基础
1. 用户与权限
   `whoami`, `su -`, `sudo`
2. 应用/包管理
   - `sudo apt-get update`, `sudo apt-get install`
3. 文件和目录
   - `ls -l`, `touch notes.txt`, `echo hello >> notes.txt`, `cat notes.txt`, `cd`
   - `chmod u+x notes.txt` (what changes? why?)
   - `pwd`, `mkdir`,`mv`,`cp`

> 如果你想学习，AI就是你最好的老师！关键是你真的在学习！

深入学生Linux，推荐鸟哥的《Linux私房菜》。

#### 实验内容 
操作系统为用户提供了3种接口来使用系统的服务：CLI, GUI和system call。

##### CLI or GUI?
根据日常使用计算机的场景，给出以下任务，思考每种任务应该使用CLI还是GUI？

- Job 1：在`~/osLabs/lab1/info`文件夹下建立20个文件:`info_1.txt`, `info_2.txt`...(tips: 使用`bash`的`for`循环)
- Job 2: 重命名Job 1中的20个文件为:`update_info_1.txt`, `update_info_2.txt`...(tips: 使用`bash`的`for`循环)
- Job 3: 假设你开发了一个C项目(程序已提供，可下载：[c_project](/Labs/lab1-interface/c_project))，发现有个字符串命名错误，需要批量修改：在`~/osLabs/lab1/c_project`文件夹下搜索所有含有`'Hello World'`字符串的文件，并替换成`'Hello OS'`.(tips: 使用`grep`+`xargs`)
- Job 4: 比较两个相似的文件的不同，已提供示例文件：`students_v1.csv`和`students_v2.csv`。(tips: 使用`diff`和`meld`)
- Job 5: 裁剪一个图片的指定区域并保存为新的文件，示例图片:[linux.png](/Labs/lab1-interface/linux.png)    
  ![linux.png](/Labs/lab1-interface/linux.png)
  裁剪要求：只保留企鹅，不要Linux文字。（tips: 使用`imagemagick`的`convert`或者`gthumb`）
- Job 6: 移动同名文件是否覆盖？（tips: 命令行`cp`和图形界面`nautilus`）
- Job 7: 从网上下载5个不同的"苹果"的图片到`~/osLabs/lab1/appels`，选择一个"看上去"最好的放入`~/osLabs/lab1/best_apple`。(tips: `wget url`)

##### 系统调用 system call
其实，不管是CLI还是GUI，最终都会通过system call来完成真正的操作。但是我们仍然把系统调用单独拿出来说，是因为它相比于CLI和GUI更直接地与系统"对话"，是用户通过编写程序使用OS提供的服务的常用接口。

下面，给出一个Python实现的，通过系统调用的方式拷贝文件的[程序](/Labs/lab1-interface/sys_call_copy.py)，且每次拷贝文件时都打印：`OS COPIED x bytes from [src-filename] to [dst-filename]`：

```py
#sys_call_copy.py
import os, sys
BUFSZ = 8192
def copy_syscalls(src, dst):
    src_fd = os.open(src, os.O_RDONLY)
    dst_fd = os.open(dst, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
    total = 0
    try:
        while True:
            chunk = os.read(src_fd, BUFSZ)
            if not chunk: break
            n = os.write(dst_fd, chunk)
            total += n
        os.fsync(dst_fd)
    finally:
        os.close(src_fd)
        os.close(dst_fd)
    print(f"OS COPIED {total} bytes from {src} to {dst}.")

if __name__ == "__main__":
    if len(sys.argv)!=3:
        print("Usage: python3 sys_call_copy.py SRC DST"); sys.exit(2)
    copy_syscalls(sys.argv[1], sys.argv[2])
```
(1) 使用到的系统调用：
+ 打开文件(获得文件描述符file descriptor)：`os.open()`
+ 读文件:`os.read()`
+ 写文件:`os.write()`
+ 将缓存内容同步到磁盘：`os.fsync()`
+ 关闭文件(释放文件描述符)：`os.close()`

(2)使用到的`os.open()`的flags：
 + `os.O_RDONLY`(0):只读
 + `os.O_WRONLY`(1):只写
 + `os.O_CREAT`(256):不存在则创建
 + `os.O_TRUNC`(512):有内容则清空
 + 其他常用flag:
   + `os.O_RDWR` − 读和写
   + `os.O_NONBLOCK` - 读写都不能打断，还记得Linux进程的状态**D**吗？
   + `os.O_APPEND ` - 写时追加内容

(3)Linux文件权限：
+ 可写`w`：2
+ 可读`r`：4
+ 可运行`x`：1
+ 用户分类：u(ser), g(roup), o(thers), a(all)
+ 程序中`0o644`: owner: 6=可读写，group: 4(可读)，other: 4(可读)
+ `chmod`,`chown`,`chgrp`

#### 实验要求
1. 从Job 1 - Job 7中选择完成：
     + 使用CLI命令行： 至少4个Job，列出命令和输出，并作解释
     + 使用GUI图形界面:至少1个，给出截屏体现过程和结果
2. 系统调用：仿照`sys_call_copy.py`通过系统调用实现一种定制化的功能，对程序做必要的解释，并给出证据证明程序的功能。
3. 思考三种接口的特点：
   - **GUI**: Discoverability, visual feedback, precision with spatial manipulation, one-off tasks.
   - **CLI**: Speed, automation, composability, reproducibility.
   - **System Calls**: custom tools, performance control, special permissions.

#### 报告提交
前往 SUNJUDGE:https://judge.xuelongsun.cn 查看实验报告模板，具体提交要求，截止时间等，并按时提交实验报告。

>注：如果你第一次使用Linux系统，你可能会很不习惯，而且可能出现各种Bug, 不要怕，solve it，我相信最终你会感受到Windows无法带给你的计算机使用体验！
