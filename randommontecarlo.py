# Contains the functions required to estimate the area of the Mandelbrot set using pure random sampling

import numpy as np
import random
import sys

# Defines basic parameters and the domain of the mandelbrot set
max_iterations = [100, 500, 1000, 2500]
N_list = [100, 1000, 10000, 100000]
alg_iterations = 100

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

def MonteCarlo(N, recursions):
    """
    Performs the MonteCarlo simulation, takes number of recursions and random variables. Returns
    """
    correct = 0

    # Generates random compelx number and checks if its in the mandelbrot set
    for _ in range(N):
        if mandelbrot(np.random.uniform(-1.79, 0.47) + np.random.uniform(-1, 1)*1j, recursions) == recursions:
            correct += 1

    # calculates area
    surface = (0.47 + 1.79) * 2 * correct / N
    
    return surface

if __name__ == '__main__':

    # Loops over max recursions in the mandelbrot set and number of random samples
    for recursions in max_iterations:
        areas = []
        area_stds = []
        for i in N_list:
            area_list = []
            for _ in range(alg_iterations):

                # Get area
                area = MonteCarlo(i, recursions)
                area_list.append(area)

            # Determine mean and std
            areas.append(np.mean(np.array(area_list)))
            area_stds.append(np.std(np.array(area_list)))

        # Determine confidence_radius
        areas = np.array(areas)
        area_stds = np.array(area_stds)

        conf_radii = area_stds*1.96/np.sqrt(alg_iterations)

        # Saves resuts to .csv file
        file_aux = open(f'results_randomfull_{recursions}.csv','a')
        file_aux.write("N_points,Mean_surface,Std_surface,confidence_radius")

        for mean, N, conf, std in zip(areas, N_list, conf_radii, area_stds):
            print(f"Sample per run {N}, Mean {mean}, Confidence radius {conf}, Max recursions {recursions}")

            file_aux.write("\n"+str(N)+","+str(mean)+","+str(std)+ ","+str(conf))

        file_aux.close()
