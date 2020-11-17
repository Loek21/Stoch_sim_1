# Creates picture of the mandelbrot set

import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
from IPython.display import display

# defines basic parameters and mandelbrot set dimensions
real_s = -1.79
real_e = 0.47
imag_s = -1
imag_e = 1

w = 400
h = 400
max_iterations = 250

def mandelbrot(c):
    """
    Takes a complex number and a max number of Iterations to calculates the number of recursions before
    the number diverges, continues untill the max iterations has been reached. Returns number of iterations before divergence.
    """
    z = 0
    n = 0
    while abs(z) <= 2 and n < max_iterations:
        z = z*z + c
        n += 1

    return n

# Creates HSV image
image = Image.new('HSV', (w, h), (0,0,0))
draw = ImageDraw.Draw(image)
points = []
area = 0
for x in range(0, w):
    for y in range(0, h):
        
        # Convert pixel coordinate to complex number
        complex = (real_s + (x / w) * (real_e - real_s)) + (imag_s + (y / h) * (imag_e - imag_s))*1j
        iters = mandelbrot(complex)
        val = 255 if iters < max_iterations else 0
        color = 255 if iters < 2 else int(iters * 500 / max_iterations)
        points.append(iters)
        draw.point([x, y], (color, 255, val))

rgb_image = image.convert(mode="RGB")
rgb_image.save("output5.png")
