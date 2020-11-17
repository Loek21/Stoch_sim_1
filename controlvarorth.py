import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import random

max_iterations = [100, 500, 1000, 2500]
repeats = [100]
N_samples = [100,1000,10000]

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

def circle(r, x, y, x_centre):

    if (x-x_centre)**2 + y**2 <= r**2:
        return True

    return False

def orthogonal(height, width, max):
    sub_size = int(np.sqrt(width))
    grid_list = []
    for i in np.arange(0, sub_size**2, sub_size):
        for j in np.arange(0, sub_size**2, sub_size):
            grid_list.append((i,j))
    height_list = [i for i in range(sub_size**2)]
    width_list = [i for i in range(sub_size**2)]
    correct = 0
    correct_circle = 0
    correct_cardioid = 0
    for grid in grid_list:
        height_range = np.logical_and(height_list >= grid[1], height_list < grid[1] + sub_size)
        height_ind = np.where(height_range)[0]
        height_pos = random.choice(height_ind)
        random_height = int(height_list[height_pos])
        width_range = np.logical_and(width_list >= grid[0], width_list < grid[0] + sub_size)
        width_ind = np.where(width_range)[0]
        width_pos = random.choice(width_ind)
        random_width = int(width_list[width_pos])
        real_number = x_start + (random_width/sub_size**2) * (x_end-x_start)
        imag_number = y_start + (random_height/sub_size**2) * (y_end-y_start)
        complex_number = real_number + imag_number*1j
        iterations = mandelbrot(complex_number, max)
        if iterations == max:
            correct += 1
        height_list.remove(random_height)
        width_list.remove(random_width)

        if circle(0.6, real_number, imag_number, -0.2):
            correct_cardioid += 1
        if circle(0.2, real_number, imag_number, -1):
            correct_circle += 1

    return correct, correct_cardioid, correct_circle

def MonteCarlo(N, height, width, max):

    correct, correct_cardioid, correct_circle = orthogonal(height, width, max)

    surface = ((abs(x_start) + abs(x_end))*(abs(y_start) + abs(y_end))) * correct/N

    surface_cardioid = ((abs(x_start) + abs(x_end))*(abs(y_start) + abs(y_end))) * correct_cardioid/N

    surface_circle = ((abs(x_start) + abs(x_end))*(abs(y_start) + abs(y_end))) * correct_circle/N

    return surface, surface_cardioid + surface_circle

def MonteCarloCircle(N, max):
    # radius cardioid 0.6 centre -0.2
    # radius circle 0.2 centre -1

    pass

def analysis(mandelbrot_areas, circle_areas, N):
    var_y = np.std(circle_areas)
    var_x = np.std(mandelbrot_areas)
    cov_xy = np.cov(mandelbrot_areas, circle_areas)
    #print(mandelbrot_areas)
    #print(circle_areas, np.mean(circle_areas))

    c = -cov_xy[0][1]/var_y
    # print(c)

    var = (var_x - c*cov_xy[0][1])/N
    for i in range(len(circle_areas)):
        circle_areas[i] -= (0.6**2 + 0.2**2) * np.pi

    #print(circle_areas)
    # print(c*circle_areas)
    area_star = mandelbrot_areas + c*(circle_areas)
    area_mean = np.mean(area_star)

    return area_mean, np.sqrt(var)



file_aux  = open(f'results_controlvarorth.csv','a')
file_aux.write("Iterations,N_points,Mean_surface,Std_surface,Confidence_radius")
for iterations in max_iterations:
    for dim in N_samples:
        surface_list = []
        circle_list = []
        N = int(np.sqrt(dim)) * int(np.sqrt(dim))
        for i in range(repeats[0]):
            surface, surface_circle = MonteCarlo(N, dim, dim, iterations)
            surface_list.append(surface)
            circle_list.append(surface_circle)
            print(f"{iterations}, {dim}, {i}")
        mean, std = analysis(np.array(surface_list), np.array(circle_list), N)
        conf = (1.96*std)/np.sqrt(repeats[0])
        file_aux.write("\n"+str(iterations)+","+str(N)+","+str(mean)+","+str(std)+","+str(conf))

file_aux.close()
