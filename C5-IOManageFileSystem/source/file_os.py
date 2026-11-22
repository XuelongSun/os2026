import os
path = "hello.txt"

fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
try:
    msg = b"Hello OS\n"
    written = os.write(fd, msg)
    if written != len(msg):
        SystemExi(1)
finally:
    os.close(fd)         

fd = os.open(path, os.O_RDONLY)
try:
    buf = os.read(fd, 32)
finally:
    os.close(fd)
os.write(1, buf) 

try:
    os.unlink(path)
except OSError:
    SystemExi(1)
