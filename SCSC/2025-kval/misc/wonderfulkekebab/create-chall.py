#!/usr/bin/env python3

from PIL import Image, ImageFont, ImageDraw

FLAG = 'SNHT{I_d1dnt_kn0w_c0mput3r5_stutt3r3d}'

im = Image.open('./source-img.png')
draw = ImageDraw.Draw(im)
font = ImageFont.truetype('./Tuffy_Bold.ttf', 16)
draw.text((0, 0), FLAG, (255, 255, 255), font=font)
im.save('/tmp/flag-img.png')

file = open('/tmp/flag-img.png', 'rb')
out_file = open('chall.bin', 'wb')
while (data := file.read(16)) != b'':
    out_file.write(data)
    out_file.write(data)
