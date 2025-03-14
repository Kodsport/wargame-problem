#!/usr/bin/env python3

import math
import struct

file = open('flag.stl', 'rb')

file.read(80)
triangle_count = int.from_bytes(file.read(4), 'little')

last_position = None
triangles = []
letters = []
for i in range(triangle_count):
    triangle = []
    for k in range(4):
        vec = [
            struct.unpack('f', file.read(4))[0],
            struct.unpack('f', file.read(4))[0],
            struct.unpack('f', file.read(4))[0],
        ]
        triangle.append(vec)
    file.read(2)
    triangles.append(triangle)

    new_position = [sum(triangle[i][j] for i in range(3)) / 3 for j in range(3)]
    if last_position is not None:
        distance = math.sqrt(sum((last_position[i] - new_position[i]) ** 2 for i in range(3)))
        if 2 < distance:
            letters.append(triangles.copy())
            triangles = []

    last_position = new_position
letters.append(triangles.copy())

data = bytearray()
data += b'\x00' * 80
data += sum(len(triangles) for triangles in letters).to_bytes(4, 'little')
for letter_i, triangles in enumerate(letters):
    for triangle in triangles:
        for j, vec in enumerate(triangle):
            j = 1
            data += struct.pack('f', vec[0] + (0 if j == 0 else (letter_i-triangles[0][1][0])))
            data += struct.pack('f', vec[1] + (0 if j == 0 else -triangles[0][1][1]))
            data += struct.pack('f', vec[2] + (0 if j == 0 else -triangles[0][1][2]))
        data += (0).to_bytes(2, 'little')

out_file = open(f'./solved.stl', 'wb')
out_file.write(data)
out_file.close()
