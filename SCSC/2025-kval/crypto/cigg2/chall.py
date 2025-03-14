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
sig1 = priv_key.sign(H(b':)'), (12*k**2 + 34*k + 56) % order)
sig2 = priv_key.sign(H(b':O'), (78*k**2 + 91*k + 23) % order)
s1, r1 = int(sig1.s), int(sig1.r)
s2, r2 = int(sig2.s), int(sig2.r)
print(f'{(r1, s1) = }')
print(f'{(r2, s2) = }')

# (r1, s1) = (110283567045318758469442063002397481452979062022926130053200576520573697515456, 28699312658401143285202819600819596869096427238907283028141247398860721160290)
# (r2, s2) = (25084667281873370801060029579797831942459353865199720453623357691990717712033, 71874976256583648925987665879651607746951533883798284039658373045535117746023)