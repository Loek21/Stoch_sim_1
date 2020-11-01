import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import random

# max_iterations = [100,500,1000,1500]
max_iterations = [1500]
width = 600
height = 400
type = "ortho"

def mandelbrot(c, max):
  z = 0
  n = 0

  while n < max and abs(z) <= 2:
    z = z**2 + c
    n += 1

  return n

def point_list(max):
    image = Image.new('RGB', (width, height), (0,0,0))
    draw = ImageDraw.Draw(image)

    x_start = -2
    x_end = 1
    y_start = -1
    y_end = 2


    saved_points = []

    for x in range(width):
      for y in range(height):

        real_number = x_start + (x/width) * (x_end-x_start)
        imag_number = y_start + (y/width) * (y_end-y_start)
        complex_number = real_number + imag_number*1j
        iters = mandelbrot(complex_number, max)

        if iters == max:
            saved_points.append((x, y))

        color = 255 - int(iters * 255 / max)
        draw.point([x, y], (color, color, color))

    # image.save('output.png', 'PNG')
    return saved_points

def pure_random():
    random_x = random.randint(0, width)
    random_y = random.randint(0, height)
    return (random_x, random_y)

def hypercube(pointlist):
    choice_list = [i for i in range(width)]
    correct = 0
    for i in range(height):
        random_int = random.choice(choice_list)
        choice_list.remove(random_int)
        if (random_int, i) in pointlist:
            correct += 1

    return correct

def orthogonal(pointlist, neighbourhood_size):
    width_list = [i for i in np.arange(0,width,neighbourhood_size)]
    height_list = [i for i in np.arange(0,height,neighbourhood_size)]
    choice_list = [i for i in range(neighbourhood_size)]
    correct = 0
    for h in height_list:
        random_width = random.choice(choice_list)
        random_height = random.choice(choice_list)
        random_width_pos = random.choice(width_list)
        width_list.remove(random_width_pos)
        if (random_width_pos+random_width, h+random_height) in pointlist:
            correct += 1

    return correct


def MonteCarlo(pointlist, N, type, neighbourhood_size):

    if type == "random":
        correct = 0

        for _ in range(N):

            if pure_random() in pointlist:
                correct += 1

    if type == "hyper":
        correct = hypercube(pointlist)

    else:
        correct = orthogonal(pointlist, neighbourhood_size)

    surface = 6 * correct/N

    return surface, correct

if type == "random":

    for max in max_iterations:
        file_aux  = open(f'results_{type}_{max}.csv','a')
        file_aux.write("N_points,Mean_surface,Std_surface")
        saved_points = point_list(max)
        for N in [100, 1000, 10000, 100000]:
            surface_list = []
            for i in range(5):
                surface, correct = MonteCarlo(saved_points, N, type, 0)
                surface_list.append(surface)
            mean = np.mean(surface_list)
            std = np.std(surface_list)
            file_aux.write("\n"+str(N)+","+str(mean)+","+str(std))

        file_aux.close()

if type == "hyper":
    N = height
    for max in max_iterations:
        file_aux  = open(f'results_{type}_{max}.csv','a')
        file_aux.write("N_points,Mean_surface,Std_surface")
        saved_points = point_list(max)
        surface_list = []
        for i in range(20):
            surface, correct = MonteCarlo(saved_points, N, type, 0)
            surface_list.append(surface)
        mean = np.mean(surface_list)
        std = np.std(surface_list)
        file_aux.write("\n"+str(N)+","+str(mean)+","+str(std))

        file_aux.close()

if type == "ortho":

    for max in max_iterations:
        file_aux  = open(f'results_{type}_{max}.csv','a')
        file_aux.write("N_points,Mean_surface,Std_surface")
        saved_points = point_list(max)
        for neighbourhood_size in range(1,6):
            N = round(height / neighbourhood_size,0)
            surface_list = []
            for i in range(50):
                surface, correct = MonteCarlo(saved_points, N, type, neighbourhood_size)
                surface_list.append(surface)
            mean = np.mean(surface_list)
            std = np.std(surface_list)
            file_aux.write("\n"+str(N)+","+str(mean)+","+str(std))

        file_aux.close()
