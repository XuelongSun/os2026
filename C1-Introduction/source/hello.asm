global _start

section .data
    msg db "Hello World", 10
    len equ $ - msg

section .text

_start:
    mov rax, 1
    mov rdi, 1
    lea rsi, [rel msg]
    mov rdx, len
    syscall

    mov rax, 60
    xor rdi, rdi
    syscall
