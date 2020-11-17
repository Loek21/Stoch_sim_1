# Contains the functions required to estimate the area of the Mandelbrot set using latin hypercube sampling

import numpy as np
import random

# Defines basic parameters and the domain of the mandelbrot set
max_iterations = [1000, 2500]
repeats = [100]
N_samples = [100,1000,10000,100000]

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

def hypercube(height, width, max):
    """
    Performs the latin hypercube sampling. Takes the dimensions of the search space and the max iterations for the mandelbrot set.
    Returns number of points that fall within the mandelbrot set, and the number of control variate.
    """
    # calculates dimension of grid cells so that both dimensions are equal
    sub_size = int(np.sqrt(width))**2
    width_list = [i for i in range(sub_size)]
    height_list = [i for i in range(sub_size)]
    correct = 0

    # Defines dimension lists from where a posiion can be selected
    for height in height_list:
        random_width = random.choice(width_list)
        real_number = x_start + (random_width/sub_size) * (x_end-x_start)
        imag_number = y_start + (height/sub_size) * (y_end-y_start)
        complex_number = real_number + imag_number*1j
        iterations = mandelbrot(complex_number, max)

        # Checks if random position is in the mandelbrot set
        if iterations == max:
            correct += 1
        width_list.remove(random_width)

    return correct

def MonteCarlo(N, height, width, max):
    """
    Performs the Monte Carlo simulation, returns surface of mandelbrot set and control variate
    """

    correct = hypercube(height, width, max)

    surface = ((abs(x_start) + abs(x_end))*(abs(y_start) + abs(y_end))) * correct/N

    return surface, correct


# Performs simulation and provides results in a .csv file
if __name__ == "__main__":
    file_aux  = open(f'results_hyper.csv','a')
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
