import sys
from ctypes import pythonapi as libc

iters = 1000000
flag = b'SNHT{v1lk3n_s1Da_sM0r4r_dU_pa_d1Tt_kN4ck3Br0d?}'
flaglen = len(flag)

buf = bytearray(flag)
libc.srand(1337)
for i in reversed(range(flaglen)):
    j = libc.rand() % (i + 1)
    buf[i], buf[j] = buf[j], buf[i]

for i in range(iters):
    i, j, k = [libc.rand() % flaglen for _ in range(3)]
    if i == j or j == k or i == k:
        continue
    buf[i] ^= buf[j]
    buf[j] ^= buf[k]
    buf[k] ^= buf[i]

with open('config.h', 'w') as f:
    f.write(f'''
#define ITERS {iters}
#define FLAG_LEN {flaglen}
char target[FLAG_LEN+1] = {{{", ".join(map(str, buf))}, 0}};         
''')