#include <fcntl.h>
#include <unistd.h>

int main(void) {
    int fd = open("hello.txt",
                  O_WRONLY | O_CREAT | O_TRUNC,
                  0644);
    if (fd == -1) return 1;

    const char msg[] = "Hello OS\n";
    if (write(fd, msg, sizeof(msg) - 1)
        != sizeof(msg) - 1) {
        close(fd);
        return 1;
    }
    if (close(fd) == -1) return 1;

    char buf[32];
    fd = open("hello.txt", O_RDONLY);
    if (fd == -1) return 1;

    ssize_t n = read(fd, buf, sizeof(buf));
    if (n < 0) {
        close(fd);
        return 1;
    }
    write(STDOUT_FILENO, buf, (size_t)n);
    close(fd);

    return unlink("hello.txt") == -1;
}
