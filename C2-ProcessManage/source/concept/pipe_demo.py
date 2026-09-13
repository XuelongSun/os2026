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
