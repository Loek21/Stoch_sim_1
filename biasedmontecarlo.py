import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import random
import sys

# max_iterations = [100,500,1000,1500]
max_iterations = [1500]
width = 600
height = 400

def mandelbrot(c, max):
  z = 0
  n = 0

  while n < max and abs(z) <= 2:
    z = z**2 + c
    n += 1

  return n

def point_list(max):
    # image = Image.new('RGB', (width, height), (0,0,0))
    # draw = ImageDraw.Draw(image)

    x_start = -2
    x_end = 1
    y_start = -1
    y_end = 2

    segment_1_points = []
    segment_2_points = []
    segment_3_points = []

    for x in range(width):
      for y in range(height):

        real_number = x_start + (x/width) * (x_end-x_start)
        imag_number = y_start + (y/width) * (y_end-y_start)
        complex_number = real_number + imag_number*1j
        iters = mandelbrot(complex_number, max)

        if iters == max:
            if y >= 200:
                if x > 121 and x < 149:
                    segment_1_points.append((x,y))
                elif x >= 149  and x < 250:
                    segment_2_points.append((x,y))
                elif x >= 250 and x < 484:
                    segment_3_points.append((x,y))

        # color = 255 - int(iters * 255 / max)
        # draw.point([x, y], (color, color, color))

    #image.save('output.png', 'PNG')
    return segment_1_points, segment_2_points, segment_3_points

def pure_random(px_start, px_end):
    random_x = random.randint(px_start, px_end)
    random_y = random.randint(200, 400)
    return (random_x, random_y)

def MonteCarlo(N, iterations, point_list):

    # get all the mandelbrot points of the specific segments
    segment_1_points, segment_2_points, segment_3_points = point_list

    # implement bias based on the fraction of correct points
    segment_1_fraction = 0.077 #28
    segment_2_fraction = 0.278 #101
    segment_3_fraction = 1 - segment_1_fraction - segment_2_fraction #234

    surface_1 = 0
    surface_2 = 0
    surface_3 = 0

    for _ in range(iterations):
        N_1 = round(segment_1_fraction * N) + 1
        N_2 = round(segment_2_fraction * N) + 1
        N_3 = round(segment_3_fraction * N) + 1

        #print(N_1, N_2, N_3)

        correct_1 = 0
        correct_2 = 0
        correct_3 = 0

        for _ in range(N_1):

            if pure_random(121, 149) in segment_1_points:
                correct_1 += 1

        segment_1_fraction = correct_1/N_1
        surface_1 = (28*0.005*200*0.005) * segment_1_fraction

        for _ in range(N_2):

            if pure_random(150, 250) in segment_2_points:
                correct_2 += 1

        segment_2_fraction = correct_2/N_2
        surface_2 = (101*0.005*200*0.005) * segment_2_fraction

        for _ in range(N_3):

            if pure_random(251, 484) in segment_3_points:
                correct_3 += 1

        segment_3_fraction = correct_3/N_3
        surface_3 = (234*0.005*200*0.005) * segment_3_fraction

        # print(surface_1, surface_2, surface_3)
        # print(surface_1 + surface_2 + surface_3)


    surface = surface_1 + surface_2 + surface_3

    return surface*2

points = point_list(max_iterations[0])
areas = []
x_list = [i for i in range(400)]

for i in range(400):
    # print(i)
    for _ in range(1):
        area = MonteCarlo(i, 5, points)
        areas.append(area)
        # plt.plot(i, area, 'ro')
plt.plot(x_list, areas)
plt.show()
