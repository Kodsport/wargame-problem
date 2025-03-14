from sage.all import *
from itertools import batched

set_random_seed(0)

flag = b'GIVEMEMYTHINGSBACK'

n = len(flag)
assert n%2 == 0

sol = vector(CC, batched(flag, 2))
mat = random_matrix(CC, n//2, n//2)
tgt = mat*sol

print(f'{n = }')
print('{' + ','.join(f'"{n.real()}"' + ',' + f'"{n.imag()}"' for n in mat.list()) + '}')
print('{' + ','.join(f'"{n.real()}"' + ',' + f'"{n.imag()}"' for n in tgt.list()) + '}')