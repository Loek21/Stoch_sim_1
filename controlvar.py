# Contains the functions required to estimate the area of the Mandelbrot set using Latin hypercube sampling in combination with Control varitues

import numpy as np
import matplotlib.pyplot as plt
import random

# Defines basic parameters and the domain of the mandelbrot set
max_iterations = [100, 500, 1000, 2500]
repeats = [100]
N_samples = [100,1000,10000,100000]

x_start = -1.79
x_end = 0.47
y_start = -1
y_end = 1

def mandelbrot(c, max):
    """
    Latin Hypercube sampling
    Takes a complex number and a max number of Iterations to calculates the number of recursions before
    the number diverges, continues untill the max iterations has been reached. Returns number of iterations before divergence.
    """
    z = 0
    n = 0

    while n < max and abs(z) <= 2:
        z = z**2 + c
        n += 1

    return n

def circle(r, x, y, x_centre):
    """
    Defines a circular equation and checks if random variable falls within the circle, takes the coordinate of the random variable,
    the radius and centre point of the circle. Returns boolean.
    """
    if (x-x_centre)**2 + y**2 <= r**2:
        return True

    return False

def hypercube(height, width, max):
    """
    Performs the latin hypercube sampling. Takes the dimensions of the search space and the max iterations for the mandelbrot set.
    Returns number of points that fall within the mandelbrot set, and the number of control variate.
    """
    # calculates dimension of grid cells so that both dimensions are equal
    sub_size = int(np.sqrt(width))**2

    # Defines dimension lists from where a posiion can be selected
    width_list = [i for i in range(sub_size)]
    height_list = [i for i in range(sub_size)]
    correct = 0
    correct_circle = 0
    correct_cardioid = 0

    # Loops over all rows, and selects a random column, coordinates get transformed into complex number
    for height in height_list:
        random_width = random.choice(width_list)
        real_number = x_start + (random_width/sub_size) * (x_end-x_start)
        imag_number = y_start + (height/sub_size) * (y_end-y_start)
        complex_number = real_number + imag_number*1j
        iterations = mandelbrot(complex_number, max)

        # Checks if complex number falls in the mandelbrot set
        if iterations == max:
            correct += 1

        # Removes column from selection possibilites
        width_list.remove(random_width)

        # Checks if variable falls in the control variates
        if circle(0.6, real_number, imag_number, -0.2):
            correct_cardioid += 1
        if circle(0.2, real_number, imag_number, -1):
            correct_circle += 1

    return correct, correct_cardioid, correct_circle

def MonteCarlo(N, height, width, max):
    """
    Performs the Monte Carlo simulation, returns surface of mandelbrot set and control variate
    """
    correct, correct_cardioid, correct_circle = hypercube(height, width, max)

    surface = ((abs(x_start) + abs(x_end))*(abs(y_start) + abs(y_end))) * correct/N

    surface_cardioid = ((abs(x_start) + abs(x_end))*(abs(y_start) + abs(y_end))) * correct_cardioid/N

    surface_circle = ((abs(x_start) + abs(x_end))*(abs(y_start) + abs(y_end))) * correct_circle/N

    return surface, surface_cardioid + surface_circle

def analysis(mandelbrot_areas, circle_areas, N):
    """
    Computes and returns the mean and variance of the mandelbrot set area, takes the areas of the set and variate and the number of random variables.
    """
    var_y = np.std(circle_areas)
    var_x = np.std(mandelbrot_areas)
    cov_xy = np.cov(mandelbrot_areas, circle_areas)

    c = -cov_xy[0][1]/var_y

    var = (var_x - c*cov_xy[0][1])/N
    for i in range(len(circle_areas)):
        circle_areas[i] -= (0.6**2 + 0.2**2) * np.pi

    area_star = mandelbrot_areas + c*(circle_areas)
    area_mean = np.mean(area_star)

    return area_mean, np.sqrt(var)


# Performs simulation and provides results in a .csv file
if __name__ == "__main__":
    file_aux  = open(f'results_controlvar.csv','a')
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
