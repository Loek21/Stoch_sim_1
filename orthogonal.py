# Contains the functions required to estimate the area of the Mandelbrot set using orthogonal sampling

import numpy as np
import random

# Defines basic parameters and the domain of the mandelbrot set
max_iterations = [100, 500, 1000, 2500]
repeats = [100]
N_samples = [100,1000,10000, 100000]

x_start = -1.79
x_end = 0.47
y_start = -1
y_end = 1

def mandelbrot(c, max):
    """
    Takes a complex number and a max number of Iterations to calculates the number of recursions before
    the number diverges, continues untill the max iterations has been reached. Returns number of iterations before divergence.
    """
    z = 0
    n = 0

    while n < max and abs(z) <= 2:
        z = z**2 + c
        n += 1

    return n

def orthogonal(height, width, max):
    """
    Orthogonal sampling.
    Takes a complex number and a max number of Iterations to calculates the number of recursions before
    the number diverges, continues untill the max iterations has been reached. Returns number of iterations before divergence.
    """
    # calculates dimension of the subgrid cells so that both dimensions are equal
    sub_size = int(np.sqrt(width))
    grid_list = []
    for i in np.arange(0, sub_size**2, sub_size):
        for j in np.arange(0, sub_size**2, sub_size):
            grid_list.append((i,j))
    height_list = [i for i in range(sub_size**2)]
    width_list = [i for i in range(sub_size**2)]
    correct = 0

    # Loops over all subgrid cells and selects an unoccupied row, column combination with this cell
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

        # Checks if random complex number is in the mandelbrot set
        if iterations == max:
            correct += 1

        # Removes grid cell, row and column from available options
        height_list.remove(random_height)
        width_list.remove(random_width)

    return correct

def MonteCarlo(N, height, width, max):
    """
    Performs the Monte Carlo simulation, returns surface of mandelbrot set and control variate
    """
    correct = orthogonal(height, width, max)

    surface = ((abs(x_start) + abs(x_end))*(abs(y_start) + abs(y_end))) * correct/N

    return surface, correct

# Performs simulation and provides results in a .csv file
if __name__ == '__main__':
    file_aux  = open(f'results_ortho_100k.csv','a')
    file_aux.write("Iterations,N_points,Mean_surface,Std_surface,Confidence_radius")
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
