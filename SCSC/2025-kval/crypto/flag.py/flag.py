import functools, operator, random
random.seed(31337)
print((functools.reduce(operator.xor, (random.getrandbits(256) for _ in range(73133736**7)))^0x458d5dbe9dd57b3a8780cfe94cbb36f14bf4f33ce4179eccecb4bd674de26d47).to_bytes(32, 'big').decode())