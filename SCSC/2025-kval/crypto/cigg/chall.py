import os
import ecdsa
import secrets
import hashlib

gen = ecdsa.NIST256p.generator
order = gen.order()

flag = os.getenv('FLAG', 'SNHT{test_flag}').encode()
assert len(flag) <= 32-2
d = int.from_bytes(b'\0\1' + flag + os.urandom(32-2-len(flag)), 'big')

pub_key = ecdsa.ecdsa.Public_key(gen, gen * d)
priv_key = ecdsa.ecdsa.Private_key(pub_key, d)

def H(m):
    return int.from_bytes(hashlib.sha256(m).digest(), 'big') % order

k = secrets.randbelow(order)
sig1 = priv_key.sign(H(b':)'), 6*k**17 + 13*k - 3*k**8*k**9 - k*20 ---k**2*k**15*3 + 8*k)
sig2 = priv_key.sign(H(b':O'), 15*k**13 - 16*k - 23*k**9*k**4 + 12*k + 8*k**5*k**8 + k*5)
s1, r1 = int(sig1.s), int(sig1.r)
s2, r2 = int(sig2.s), int(sig2.r)
print(f'{(r1, s1) = }')
print(f'{(r2, s2) = }')

# (r1, s1) = (75500473885933440102349250800371371719844218835306589569739362373352510711748, 16024164171116223134077765902232407130958988685148352157522953597450963414049)
# (r2, s2) = (75500473885933440102349250800371371719844218835306589569739362373352510711748, 4694071681235633686740348059417161949764482691159381333680771208497833303204)