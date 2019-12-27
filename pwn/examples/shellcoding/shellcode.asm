[BITS 64]

_start:
    ; zerujemy argumenty argv i envp
    xor esi, esi
    xor edx, edx
    ; napis "/bin/sh\x00" spakowany jako 64bitowa liczba
    mov rax, 0x68732f6e69622f
    ; ustawiamy wskaźnik na niego w 1 argumencie
    push rax
    mov rdi, rsp
    ; execve
    mov eax, 0x3b
    syscall
