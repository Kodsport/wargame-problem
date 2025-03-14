from base64 import b64encode
from Crypto.Util.strxor import strxor

flag = b"SNHT{b64_puts_a_twist_on_th1s_oth3rw1se_3asy_pr0blem}"
english_sentence = b'One-time pads are "information-theoretically secure".'

assert len(flag) == len(english_sentence)

# ct = strxor(flag, english_sentence)  # This would be too easy
ct = strxor(b64encode(flag), b64encode(english_sentence))  # Have fun

print(ct.hex())
# ct.hex() == "010200251a1026192c3d0701000f105b00487b003b5e075428352245025f000c3a64145f2c0f77132e6b00001764734a17001c1c0148081b017b0701007a1f1d3d3532002b310400"
