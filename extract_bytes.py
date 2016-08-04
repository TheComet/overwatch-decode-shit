from scipy import misc
from math import radians, cos, sin

arr = misc.imread('image.png')
sectors = 128
angle_offset = (360.0 / sectors / 4 * 3)  # tweaked until it looked right
offset = 123
width = 149
center = (267, 267)

def gen_angles():
    for angle in [360.0 * sector / sectors for sector in range(sectors)]:
        yield angle + angle_offset

def gen_offsets():
    for angle in gen_angles():
        for bit in range(8):
            x = cos(radians(angle)) * (width * bit / 8.0 + offset) + center[0]
            y = sin(radians(angle)) * (width * bit / 8.0 + offset) + center[1]
            yield int(x), int(y)

def bit_stream():
    for x, y in gen_offsets():
        color = arr[x, y]
        if color[0] > 127 and color[1] > 127 and color[2] > 127:
            yield 1
        else:
            yield 0

def byte_stream():
    accumulate = 0
    count = 0
    for bit in bit_stream():
        accumulate = accumulate | (bit << count)
        count += 1
        if count == 8:
            yield accumulate
            accumulate = 0
            count = 0

def debug_output():
    for x, y in gen_offsets():
        arr[x, y] = (255, 0, 0, 0)
    
    misc.imsave('image_out.png', arr)

if __name__ == '__main__':
    with open('out.txt', 'w') as f:
        for byte in byte_stream():
            f.write(str(byte) + " ")
