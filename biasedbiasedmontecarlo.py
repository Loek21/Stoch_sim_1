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

def MonteCarlo(iterations, point_list):

    # get all the mandelbrot points of the specific segments
    segment_1_points, segment_2_points, segment_3_points = point_list
    total_points = len(segment_1_points) + len(segment_2_points) + len(segment_3_points)
    # implement bias based on the fraction of correct points
    segment_1_fraction = len(segment_1_points)/total_points
    segment_2_fraction = len(segment_2_points)/total_points
    #segment_3_fraction = len(segment_3_points)/total_points

    surface_1 = 0
    surface_2 = 0
    surface_3 = 0

    N_1 = 1
    N_2 = 1
    N_3 = 1

    correct_1 = 0
    correct_2 = 0
    correct_3 = 0

    surface_list = []

    for _ in range(iterations):

        surface_1 = (28*0.005*200*0.005) * correct_1 / N_1
        surface_2 = (101*0.005*200*0.005) * correct_2 / N_2
        surface_3 = (234*0.005*200*0.005) * correct_3 / N_3
        surface = surface_1 + surface_2 + surface_3
        surface_list.append(2*surface)

        random = np.random.uniform(0,1)
                
        if random < segment_1_fraction:
            N_1 += 1

            if pure_random(121, 149) in segment_1_points:
                correct_1 += 1

        elif random > segment_1_fraction and random < segment_1_fraction + segment_2_fraction:
            N_2 += 1

            if pure_random(150, 250) in segment_2_points:
                correct_2 += 1
        
        else:
            N_3 += 1

            if pure_random(251, 484) in segment_3_points:
                correct_3 += 1

    return np.array(surface_list)

points = point_list(150)
areas = []


for _ in range(5):
    area = MonteCarlo(201, points)


plt.plot(np.arange(0,201,1), area)

plt.show()