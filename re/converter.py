#!/usr/bin/python3

from PIL import Image
import numpy as np
import sys

def read_num(Bits, index, chunk):
    ans = 0
    pow2 = 1
    for i in range(chunk):
        ans += Bits[index+i] * pow2
        pow2 *= 2
    return ans
    
if len(sys.argv) < 3:
    raise Exception("Invalid numer of arguments")

pngfile = sys.argv[2]
imgfile = sys.argv[1]

Bytes = np.fromfile(imgfile, dtype = "uint8")
Bits = np.unpackbits(Bytes, bitorder="little")

img_size_x = read_num(Bits, 0, 24)
img_size_y = read_num(Bits, 24, 24)

img = Image.new(mode='RGB', size=(img_size_x, img_size_y), color=None)

bmp = np.empty(img_size_y * img_size_x, dtype=object)

bit = 48

i = 0
n = img_size_y * img_size_x
while i < n:
    if Bits[bit] == 1:
        bit += 1
        R = read_num(Bits, bit, 8)
        G = read_num(Bits, bit + 8, 8)
        B = read_num(Bits, bit + 16, 8)
        bmp[i] = (R, G, B)
        bit += 8 * 3
        i += 1
    else:
        bit += 1
        position = read_num(Bits, bit, 5) + 1
        size = read_num(Bits, bit + 5, 5)

        j = i
        while (j < i + size):
            bmp[j] = bmp[j - position]
            j += 1

        bit += 5 * 2
        i += size

bmp = np.reshape(bmp, (-1, img_size_x))

for i in range(img_size_x):
    for j in range(img_size_y):
        img.putpixel((i, j), bmp[j][i])

img.save(f"{pngfile}")
