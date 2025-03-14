from ctypes import pythonapi as libc

buf = bytearray([33, 2, 69, 98, 58, 97, 9, 113, 112, 95, 77, 3, 85, 117, 50, 90, 119, 76, 93, 107, 114, 23, 43, 16, 111, 90, 121, 37, 76, 20, 43, 64, 1, 48, 40, 87, 93, 101, 75, 13, 59, 69, 42, 79, 125, 20, 32])
flaglen = len(buf)
iters = 1000000

libc.srand(1337)

rands = [libc.rand() for _ in range(flaglen + 3*iters)]

for i in range(iters):
    k, j, i = [rands.pop() % flaglen for _ in range(3)]
    if i == j or j == k or i == k:
        continue
    k_pre = buf[i] ^ buf[k];
    j_pre = buf[j] ^ k_pre;
    i_pre = buf[i] ^ j_pre;
    buf[i] = i_pre
    buf[j] = j_pre
    buf[k] = k_pre

for i in range(flaglen):
    j = rands.pop() % (i + 1)
    buf[i], buf[j] = buf[j], buf[i]

assert len(rands) == 0
print(buf.decode())