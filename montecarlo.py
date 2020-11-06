import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import random

# max_iterations = [100,500,1000,1500]
max_iterations = [200]
width = 600
height = 400
type = "ortho"
neighbourhood_size = 2

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


saved_points = point_list(max_iterations[0])
surface_r_arr = np.zeros((5, 400))
for i in range(5):
    correct = 0
    for N in range(1,401):
        rand_crd = pure_random()
        if rand_crd in saved_points:
            correct += 1
        surface_r_arr[i][N-1] = 6 * correct / N

mean_r = np.mean(surface_r_arr, axis=0)
std_r = np.std(surface_r_arr, axis=0)
N_list = [i for i in range(400)]
plt.plot(N_list, mean_r, label="Random")
plt.fill_between(N_list, mean_r+std_r, mean_r-std_r, alpha=0.2)



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


surface_h_arr = np.zeros((5, 400))
for i in range(5):
    correct = 0
    choice_list_w = [i for i in range(width)]
    choice_list_h = [i for i in range(1,401)]
    for N in range(1,401):
        random_int_w = random.choice(choice_list_w)
        random_int_h = random.choice(choice_list_h)
        choice_list_w.remove(random_int_w)
        choice_list_h.remove(random_int_h)
        if (random_int_w, random_int_h-1) in saved_points:
            correct += 1
        surface_h_arr[i][N-1] = 6 * correct / N

mean_h = np.mean(surface_h_arr, axis=0)
std_h = np.std(surface_h_arr, axis=0)
plt.plot(N_list, mean_h, label="Latin hypercube")
plt.fill_between(N_list, mean_h+std_h, mean_h-std_h, alpha=0.2)



# if type == "hyper":
#     N = height
#     for max in max_iterations:
#         file_aux  = open(f'results_{type}_{max}.csv','a')
#         file_aux.write("N_points,Mean_surface,Std_surface")
#         saved_points = point_list(max)
#         surface_list = []
#         for i in range(20):
#             surface, correct = MonteCarlo(saved_points, N, type, 0)
#             surface_list.append(surface)
#         mean = np.mean(surface_list)
#         std = np.std(surface_list)
#         file_aux.write("\n"+str(N)+","+str(mean)+","+str(std))
#
#         file_aux.close()
height_dim = int(height/neighbourhood_size)
surface_o_arr = np.zeros((5, height_dim))
for i in range(5):
    correct = 0
    N = 1
    width_list = [i for i in np.arange(0,width,neighbourhood_size)]
    height_list = [i for i in np.arange(0,height,neighbourhood_size)]
    choice_list = [i for i in range(neighbourhood_size)]
    for h in range(len(height_list)):
        random_width = random.choice(choice_list)
        random_height = random.choice(choice_list)
        random_width_pos = random.choice(width_list)
        random_height_pos = random.choice(height_list)
        width_list.remove(random_width_pos)
        height_list.remove(random_height_pos)
        if (random_width_pos+random_width, random_width_pos+random_height) in saved_points:
            correct += 1
        surface_o_arr[i][N-1] = 6 * correct / N
        N += 1
mean_o = np.mean(surface_o_arr, axis=0)
std_o = np.std(surface_o_arr, axis=0)
N_list_o = [i for i in range(int(400/neighbourhood_size))]
plt.plot(N_list_o, mean_o, label="Orthogonal")
plt.fill_between(N_list_o, mean_o+std_o, mean_o-std_o, alpha=0.2)
plt.legend()
plt.ylim(0,3)
plt.show()

# if type == "ortho":
#
#     for max in max_iterations:
#         file_aux  = open(f'results_{type}_{max}.csv','a')
#         file_aux.write("N_points,Mean_surface,Std_surface")
#         saved_points = point_list(max)
#         for neighbourhood_size in range(1,6):
#             N = round(height / neighbourhood_size,0)
#             surface_list = []
#             for i in range(50):
#                 surface, correct = MonteCarlo(saved_points, N, type, neighbourhood_size)
#                 surface_list.append(surface)
#             mean = np.mean(surface_list)
#             std = np.std(surface_list)
#             file_aux.write("\n"+str(N)+","+str(mean)+","+str(std))
#
#         file_aux.close()
