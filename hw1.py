import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from IPython.display import display

real_s = -2
real_e = 1
imag_s = -1
imag_e = 1

w = 600
h = 400

max_iterations = 500
def mandelbrot(c):
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iterations:
        z = z*z + c
        n += 1
    return n

image = Image.new('HSV', (w, h), (0,0,0))
draw = ImageDraw.Draw(image)
points = []
area = 0
for x in range(0, w):
    for y in range(0, h):
        # Convert pixel coordinate to complex number
        complex = (real_s + (x / w) * (real_e - real_s)) + (imag_s + (y / h) * (imag_e - imag_s))*1j
        iters = mandelbrot(complex)
        # val = 255 if iters < 80 else 0
        # color = 0 if iters < 2 else int(iters * 500 / max_iterations)
        points.append(iters)
        if iters == max_iterations:
            area += 1
            draw.point([x, y], (255, 255, 255))
        else:
            draw.point([x, y], (0,0,0))
rgb_image = image.convert(mode="RGB")
# pixels = rgb_image.load()
# print(pixels[100,100])
# for x in range(w):
#     for y in range(h):
#         r = pixels[x,y][0]
#         g = pixels[x,y][1]
#         b = pixels[x,y][2]
#         if r == 255 and g < 50 and b < 50:
#             pixels[x,y] = (0,0,0)
rgb_image.save("output4.png")

print(len(points))
print(area)
