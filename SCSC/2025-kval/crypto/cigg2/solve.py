from sage.all import polygens, ideal, Zmod

import re
import ecdsa
import hashlib

gen = ecdsa.NIST256p.generator
order = int(gen.order())

def H(m):
    return int.from_bytes(hashlib.sha256(m).digest(), 'big') % order

(r1, s1) = (110283567045318758469442063002397481452979062022926130053200576520573697515456, 28699312658401143285202819600819596869096427238907283028141247398860721160290)
(r2, s2) = (25084667281873370801060029579797831942459353865199720453623357691990717712033, 71874976256583648925987665879651607746951533883798284039658373045535117746023)

h1, h2 = H(b':)'), H(b':O')

k, d = polygens(Zmod(int(order)), 'k, d')

s1inv, s2inv = pow(s1, -1, order), pow(s2, -1, order)
I = ideal([
    (12*k**2 + 34*k + 56) - (h1*s1inv + r1*d*s1inv),
    (78*k**2 + 91*k + 23) - (h2*s2inv + r2*d*s2inv)
])
for sol in I.variety():
    raw = int(sol[d]).to_bytes(32, 'big')
    for m in re.findall(b'SNHT{[^}]*}', raw):
        print(m.decode())