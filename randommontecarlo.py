import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import random
import sys

## start at -1.79
## -1.25 tot first blob
## -0.75 tot 2nd blob
## 0.47 tot last blob
# max_iterations = [100,500,1000,1500]
max_iterations = [100, 500, 1000, 2500]
N_list = [100, 1000, 10000, 100000]
alg_iterations = 100

def mandelbrot(c, max):
  z = 0
  n = 0

  while n < max and abs(z) <= 2:
    z = z**2 + c
    n += 1

  return n

def MonteCarlo(N, recursions): 
    correct = 0

    for _ in range(N):
        if mandelbrot(np.random.uniform(-1.79, 0.47) + np.random.uniform(-1, 1)*1j, recursions) == recursions:
            correct += 1

    surface = (0.47 + 1.79) * correct / N

    return surface * 2

for recursions in max_iterations:
    areas = []
    area_stds = []
    for i in N_list:
        area_list = []
        for _ in range(alg_iterations):
            area = MonteCarlo(i, recursions)
            area_list.append(area)

        areas.append(np.mean(np.array(area_list)))
        area_stds.append(np.std(np.array(area_list)))

    areas = np.array(areas)
    area_stds = np.array(area_stds)

    #plt.plot(N_list, areas, label="Strat sampling")
    #plt.fill_between(N_list, areas+area_stds, areas-area_stds, alpha=0.2)
    #plt.plot(N_list, area_stds*1.96/np.sqrt(alg_iterations))

    conf_radii = area_stds*1.96/np.sqrt(alg_iterations)

    file_aux = open(f'results_randomfull_{recursions}.csv','a')
    file_aux.write("N_points,Mean_surface,Std_surface,confidence_radius")

    for mean, N, conf, std in zip(areas, N_list, conf_radii, area_stds):
        print(f"Sample per run {N}, Mean {mean}, Confidence radius {conf}, Max recursions {recursions}")
        
        file_aux.write("\n"+str(N)+","+str(mean)+","+str(std)+ ","+str(conf))

    file_aux.close()

    #plt.show()