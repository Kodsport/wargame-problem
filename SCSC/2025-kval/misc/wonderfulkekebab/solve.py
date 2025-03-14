#!/usr/bin/env python3

file = open('chall.bin', 'rb')
out_file = open('solved.png', 'wb')
while (data := file.read(16)) != b'':
    out_file.write(data)
    file.read(16)
out_file.close()
