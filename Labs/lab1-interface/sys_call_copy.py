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
    if len(sys.argv) != 3:
        print("Usage: python3 sys_call_copy.py SRC DST"); sys.exit(2)
    copy_syscalls(sys.argv[1], sys.argv[2])
    
