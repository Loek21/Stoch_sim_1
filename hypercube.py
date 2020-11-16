import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import random

max_iterations = [1000, 2500]
repeats = [100]
N_samples = [100,1000,10000,100000]

x_start = -1.79
x_end = 0.47
y_start = -1
y_end = 1

def mandelbrot(c, max):
  z = 0
  n = 0

  while n < max and abs(z) <= 2:
    z = z**2 + c
    n += 1

  return n

def hypercube(height, width, max):
    sub_size = int(np.sqrt(width))**2
    width_list = [i for i in range(sub_size)]
    height_list = [i for i in range(sub_size)]
    correct = 0
    for height in height_list:
        # random_height = random.choice(height_list)
        random_width = random.choice(width_list)
        real_number = x_start + (random_width/sub_size) * (x_end-x_start)
        imag_number = y_start + (height/sub_size) * (y_end-y_start)
        complex_number = real_number + imag_number*1j
        iterations = mandelbrot(complex_number, max)
        if iterations == max:
            correct += 1
        # height_list.remove(random_height)
        width_list.remove(random_width)
    return correct

def MonteCarlo(N, height, width, max):

    correct = hypercube(height, width, max)

    surface = ((abs(x_start) + abs(x_end))*(abs(y_start) + abs(y_end))) * correct/N

    return surface, correct


file_aux  = open(f'results_hyper.csv','a')
# file_aux.write("Iterations,N_points,Mean_surface,Std_surface,Confidence_radius")
for iterations in max_iterations:
    for dim in N_samples:
        surface_list = []
        N = int(np.sqrt(dim)) * int(np.sqrt(dim))
        for i in range(repeats[0]):
            surface, correct = MonteCarlo(N, dim, dim, iterations)
            surface_list.append(surface)
            print(f"{iterations}, {dim}, {i}")
        mean = np.mean(surface_list)
        std = np.std(surface_list)
        conf = (1.96*std)/np.sqrt(repeats[0])
        file_aux.write("\n"+str(iterations)+","+str(N)+","+str(mean)+","+str(std)+","+str(conf))

file_aux.close()
