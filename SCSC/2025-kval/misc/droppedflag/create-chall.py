#!/usr/bin/env python3

# Run with
# blender --background --python create-chall.py

import bpy
from pathlib import Path
import struct
import os
import random

FLAG = 'SNHT{fil3r_in3håller_m3r_info_än_väntat}'
MESH_DIR = Path('meshes')

os.makedirs(MESH_DIR, exist_ok=True)

# Blender part

bpy.ops.object.select_all(action='DESELECT')
for i, c in enumerate(FLAG):
    text = bpy.data.curves.new("char", "FONT")
    ob = bpy.data.objects.new("char", text)
    bpy.context.collection.objects.link(ob)
    ob.location = (
        random.random() * 10000,
        random.random() * 10000,
        random.random() * 10000
    )
    text.body = c
    text.extrude = 0.1

    bpy.context.view_layer.objects.active = ob
    ob.select_set(True)
    bpy.ops.export_mesh.stl(
            filepath=str(MESH_DIR / f'{i}.stl'),
            use_selection=True)
    ob.select_set(False)

# Post blender part

letters = []
for i in range(len(FLAG)):
    file = open(MESH_DIR / f'{i}.stl', 'rb')

    file.read(80)
    triangle_count = int.from_bytes(file.read(4), 'little')

    triangles = []
    for j in range(triangle_count):
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
    letters.append(triangles)

file = open('flag.stl', 'wb')

file.write(b'\x00' * 80)
file.write(sum(len(triangles) for triangles in letters).to_bytes(4, 'little'))

for triangles in letters:
    for triangle in triangles:
        for vec in triangle:
            file.write(struct.pack('f', vec[0]))
            file.write(struct.pack('f', vec[1]))
            file.write(struct.pack('f', vec[2]))
        file.write((0).to_bytes(2, 'little'))

file.close()

