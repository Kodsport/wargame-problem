from base64 import b64encode
from Crypto.Util.strxor import strxor

flag = b"SNHT{???}"
english_sentence = b'???'

assert len(flag) == len(english_sentence)

ct = strxor(b64encode(flag), b64encode(english_sentence))

print(ct.hex())
# ct.hex() == "010200251a1026192c3d0701000f105b00487b003b5e075428352245025f000c3a64145f2c0f77132e6b00001764734a17001c1c0148081b017b0701007a1f1d3d3532002b310400"

"""
Kort förklaring:
flag är i l33tspeak.
english_sentence är en typisk engelsk mening med några få special tecken.
ct.hex() kommentaren är output från riktiga flaggan. Använd den för att hitta flaggan.
Det finns oändligt många matemtiskt korrekta lösningar, men bara en som betyder något.

Detta är i princip samma problem som standard one-time pad med en återanvänd nyckel.
"""
