import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import random

max_iterations = [100, 500, 1000, 2500]
repeats = [2]
N_samples = [100,1000,10000,100000]
width = 400
height = 400
type = "ortho"

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

def point_list(max, height, width):
    image = Image.new('RGB', (width, height), (0,0,0))
    draw = ImageDraw.Draw(image)

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

def hypercube(pointlist, height, width):
    choice_list = [i for i in range(width)]
    correct = 0
    for i in range(height):
        random_int = random.choice(choice_list)
        choice_list.remove(random_int)
        if (random_int, i) in pointlist:
            correct += 1

    return correct

def orthogonal(pointlist, height, width):
    sub_size = int(np.sqrt(width))
    grid_list = []
    for i in np.arange(0, width, sub_size):
        for j in np.arange(0, height, sub_size):
            grid_list.append((i,j))
    height_list = [i for i in range(height)]
    width_list = [i for i in range(width)]
    correct = 0
    for i in range(width):
        grid = random.choice(grid_list)
        height_range = np.logical_and(height_list >= grid[1], height_list < grid[1] + sub_size)
        height_ind = np.where(height_range)[0]
        height_pos = random.choice(height_ind)
        random_height = int(height_list[height_pos])
        width_range = np.logical_and(width_list >= grid[0], width_list < grid[0] + sub_size)
        width_ind = np.where(width_range)[0]
        width_pos = random.choice(width_ind)
        random_width = int(width_list[width_pos])
        if (random_width, random_height) in pointlist:
            correct += 1
        height_list.remove(random_height)
        width_list.remove(random_width)
        grid_list.remove(grid)

    return correct


def MonteCarlo(pointlist, N, type, height, width):

    if type == "random":
        correct = 0

        for _ in range(N):

            if pure_random() in pointlist:
                correct += 1

    if type == "hyper":
        correct = hypercube(pointlist, height, width)

    else:
        correct = orthogonal(pointlist, height, width)

    surface = ((abs(x_start) + abs(x_end))*(abs(y_start) + abs(y_end))) * correct/N

    return surface, correct


# saved_points = point_list(max_iterations[0])
# surface_r_arr = np.zeros((5, 400))
# for i in range(5):
#     correct = 0
#     for N in range(1,401):
#         rand_crd = pure_random()
#         if rand_crd in saved_points:
#             correct += 1
#         surface_r_arr[i][N-1] = 6 * correct / N
#
# mean_r = np.mean(surface_r_arr, axis=0)
# std_r = np.std(surface_r_arr, axis=0)
# N_list = [i for i in range(400)]
# plt.plot(N_list, mean_r, label="Random")
# plt.fill_between(N_list, mean_r+std_r, mean_r-std_r, alpha=0.2)



# if type == "random":
#
# for max in max_iterations:
#     file_aux  = open(f'results_{type}_{max}.csv','a')
#     file_aux.write("N_points,Mean_surface,Std_surface")
#     saved_points = point_list(max)
#     for N in [100, 1000, 10000, 100000]:
#         surface_list = []
#         for i in range(5):
#             surface, correct = MonteCarlo(saved_points, N, type, 0)
#             surface_list.append(surface)
#         mean = np.mean(surface_list)
#         std = np.std(surface_list)
#         file_aux.write("\n"+str(N)+","+str(mean)+","+str(std))
#
#     file_aux.close()


# surface_h_arr = np.zeros((5, 400))
# for i in range(5):
#     correct = 0
#     choice_list_w = [i for i in range(width)]
#     choice_list_h = [i for i in range(1,401)]
#     for N in range(1,401):
#         random_int_w = random.choice(choice_list_w)
#         random_int_h = random.choice(choice_list_h)
#         choice_list_w.remove(random_int_w)
#         choice_list_h.remove(random_int_h)
#         if (random_int_w, random_int_h-1) in saved_points:
#             correct += 1
#         surface_h_arr[i][N-1] = 6 * correct / N
#
# mean_h = np.mean(surface_h_arr, axis=0)
# std_h = np.std(surface_h_arr, axis=0)
# plt.plot(N_list, mean_h, label="Latin hypercube")
# plt.fill_between(N_list, mean_h+std_h, mean_h-std_h, alpha=0.2)



if type == "hyper":
    N = height
    saved_points = point_list(max_iterations)
    file_aux  = open(f'results_{type}.csv','a')
    file_aux.write("Repeats,N_points,Mean_surface,Std_surface")
    for repeat in repeats:

        surface_list = []
        for i in range(repeat):
            surface, correct = MonteCarlo(saved_points, N, type, 0)
            surface_list.append(surface)
        mean = np.mean(surface_list)
        std = np.std(surface_list)
        file_aux.write("\n"+str(repeat)+","+str(N)+","+str(mean)+","+str(std))

    file_aux.close()

# height_dim = int(height/neighbourhood_size)
# surface_o_arr = np.zeros((5, height_dim))
# for i in range(5):
#     correct = 0
#     N = 1
#     width_list = [i for i in np.arange(0,width,neighbourhood_size)]
#     height_list = [i for i in np.arange(0,height,neighbourhood_size)]
#     choice_list = [i for i in range(neighbourhood_size)]
#     for h in range(len(height_list)):
#         random_width = random.choice(choice_list)
#         random_height = random.choice(choice_list)
#         random_width_pos = random.choice(width_list)
#         random_height_pos = random.choice(height_list)
#         width_list.remove(random_width_pos)
#         height_list.remove(random_height_pos)
#         if (random_width_pos+random_width, random_width_pos+random_height) in saved_points:
#             correct += 1
#         surface_o_arr[i][N-1] = 6 * correct / N
#         N += 1
# mean_o = np.mean(surface_o_arr, axis=0)
# std_o = np.std(surface_o_arr, axis=0)
# N_list_o = [i for i in range(int(400/neighbourhood_size))]
# plt.plot(N_list_o, mean_o, label="Orthogonal")
# plt.fill_between(N_list_o, mean_o+std_o, mean_o-std_o, alpha=0.2)
# plt.legend()
# plt.ylim(0,3)
# plt.show()

if type == "ortho":

    file_aux  = open(f'results_{type}.csv','a')
    file_aux.write("Type,Iterations,N_points,Mean_surface,Std_surface,Confidence_radius")
    for iterations in max_iterations:
        for dim in N_samples:
            saved_points = point_list(iterations, dim, dim)
            surface_list = []
            N = int(np.sqrt(dim)) * int(np.sqrt(dim))
            for i in range(repeats[0]):
                surface, correct = MonteCarlo(saved_points, N, type, dim, dim)
                surface_list.append(surface)
            mean = np.mean(surface_list)
            std = np.std(surface_list)
            conf = (1.96*std)/np.sqrt(repeats[0])
            file_aux.write("\n"+str(N)+","+str(mean)+","+str(std)+","+str(conf))

    file_aux.close()
