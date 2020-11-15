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
max_iterations = 1500
width = 600
height = 400

def mandelbrot(c, max):
  z = 0
  n = 0

  while n < max and abs(z) <= 2:
    z = z**2 + c
    n += 1

  return n

def MonteCarlo(N): 
    correct = 0

    for _ in range(N):
        if mandelbrot(np.random.uniform(-1.79, 0.47) + np.random.uniform(-1, 1)*1j, max_iterations) == max_iterations:
            correct += 1

    surface = (0.47 + 1.79) * 2 * correct / N

    return surface

areas = []
area_stds = []
N_list = [200,400,800, 1600, 5000]
alg_iterations = 100
for i in N_list:
    area_list = []
    for _ in range(alg_iterations):
        area = MonteCarlo(i)
        area_list.append(area)

    areas.append(np.mean(np.array(area_list)))
    area_stds.append(np.std(np.array(area_list)))

areas = np.array(areas)
area_stds = np.array(area_stds)

plt.plot(N_list, areas, label="Strat sampling")
plt.fill_between(N_list, areas+area_stds, areas-area_stds, alpha=0.2)
plt.plot(N_list, area_stds*1.96/np.sqrt(alg_iterations))

conf_radii = area_stds*1.96/np.sqrt(alg_iterations)

for mean, N, conf in zip(areas, N_list, conf_radii):
    print(f"Runs {N}, Mean {mean}, Confidence radius {conf}")




plt.show()