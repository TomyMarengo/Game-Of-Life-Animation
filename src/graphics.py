import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap
import sys

dimension = str(sys.argv[1])

def calculate_observables(step):
    with open('../outputs/' + dimension + '/output_' + dimension + '_' + file_suffix + '.txt', 'r') as file:
        lines = file.readlines()
    md = 0
    ac = 0

    for z in range(size_z):
        for y in range(size_y):
            for x in range(size_x):
                number = int(lines[1 + step*2][x + size_x * y + size_x * size_y * z])
                if number == 1:
                    distance_to_center = np.sqrt((x - size_x/2)**2 + (y - size_y/2)**2 + (z - size_z/2)**2)
                    if distance_to_center > md:
                        md = distance_to_center
                    ac += 1

    return md, ac

with open('../outputs/' + dimension + '/data' + dimension + '.txt', 'r') as data_file:
    data_lines = data_file.readlines()

maxRep = 5
systems = 3
data_per_system = 9
percentages = [100, 85, 70, 55, 40, 25]
inputs = len(percentages)
x_values = np.array(percentages)

max_distances_list = [[[[] for _ in range(maxRep)] for _ in range(inputs)] for _ in range(systems)]
alive_cells_list = [[[[] for _ in range(maxRep)] for _ in range(inputs)] for _ in range(systems)]

max_distances_scalars = [[[0 for _ in range(maxRep)] for _ in range(inputs)] for _ in range(systems)]
alive_cells_scalars = [[[0 for _ in range(maxRep)] for _ in range(inputs)] for _ in range(systems)]

avg_max_distances_scalars = [[0 for _ in range(inputs)] for _ in range(systems)]
std_max_distances_scalars = [[0 for _ in range(inputs)] for _ in range(systems)]
avg_alive_cells_scalars = [[0 for _ in range(inputs)] for _ in range(systems)]
std_alive_cells_scalars = [[0 for _ in range(inputs)] for _ in range(systems)]

for system in range(systems):
    for my_input in range(inputs):
        for rep in range(maxRep):
            first_line =  ( inputs * maxRep * system + maxRep * my_input + rep ) * data_per_system
            rule = str(data_lines[first_line].split()[1])
            ntype = str(data_lines[first_line+1].split()[1])
            radius = int(data_lines[first_line+2].split()[1])
            alive = int(data_lines[first_line+3].split()[1])
            max_step = int(data_lines[first_line+4].split()[1])
            size_x = int(data_lines[first_line+5].split()[1])
            size_y = int(data_lines[first_line+6].split()[1])
            size_z = int(data_lines[first_line+7] .split()[1])
            file_suffix = rule + '_' + ntype + '_' + 'r' + str(radius) + '_' + str(alive) + '_' + str(rep)
            
            max_distances_list[system][my_input][rep] = [0 for _ in range(max_step)]
            alive_cells_list[system][my_input][rep] = [0 for _ in range(max_step)]
            
            for step in range(max_step):
                max_distance, alive_cells = calculate_observables(step)
                max_distances_list[system][my_input][rep][step] = max_distance
                alive_cells_list[system][my_input][rep][step] = alive_cells
        
            max_distances_scalars[system][my_input][rep] = np.max(max_distances_list[system][my_input][rep])
            alive_cells_scalars[system][my_input][rep] = np.max(alive_cells_list[system][my_input][rep])
        
        avg_max_distances_scalars[system][my_input] = np.mean(max_distances_scalars[system][my_input])
        std_max_distances_scalars[system][my_input] = np.std(max_distances_scalars[system][my_input])
        avg_alive_cells_scalars[system][my_input] = np.mean(alive_cells_scalars[system][my_input])
        std_alive_cells_scalars[system][my_input] = np.std(alive_cells_scalars[system][my_input])
    
    graph_suffix = rule + '_' + ntype + '_' + 'r' + str(radius)
    
    
    # OUTPUT MAX DISTANCIA VS TIEMPO
    plt.figure(figsize=(10, 6))
    plt.title('Maxima distancia en funcion del tiempo')
    for i, curve_values in enumerate(max_distances_list[system]):
        time = np.arange(1, len(curve_values[0]) + 1)
        plt.plot(time, curve_values[0], label=f'{percentages[i]} %')

    plt.xlabel('Tiempo')
    plt.ylabel('Maxima distancia euclidiana al centro (Celdas)')
    plt.grid()
    plt.legend(loc='upper right')

    plt.savefig('../images/' + dimension + '/max_distance_vs_time_' + dimension + '_' + graph_suffix + '.png')
    print('max_distance_vs_time_' + dimension + '_' + graph_suffix + ' creado')
    
    # OUTPUT CANTIDAD DE CELDAS VIVAS VS TIEMPO
    plt.figure(figsize=(10, 6))
    plt.title('Cantidad de celdas vivas en funcion del tiempo')
    for i, curve_values in enumerate(alive_cells_list[system]):
        time = np.arange(1, len(curve_values[0]) + 1)
        plt.plot(time, curve_values[0], label=f'{percentages[i]} %')

    plt.xlabel('Tiempo')
    plt.ylabel('Cantidad de celdas vivas')
    plt.grid()
    plt.legend(loc='upper right')

    plt.savefig('../images/' + dimension + '/alive_cells_vs_time_' +  dimension + '_' + graph_suffix + '.png')
    print('alive_cells_vs_time_' + dimension + '_' + graph_suffix + ' creado')
    
    # OBSERVABLE MAX DISTANCIA VS INPUT
    plt.figure(figsize=(10, 6))
    plt.title('Maxima distancia por Input')
    plt.errorbar(x_values, avg_max_distances_scalars[system], yerr=std_max_distances_scalars[system], fmt='o')
    plt.xlabel('Input (%)')
    plt.ylabel('Maxima distancia euclidiana al centro (Celdas)')
    plt.xticks(x_values, percentages)
    plt.grid()
    
    plt.savefig('../images/' + dimension + '/obs_max_distance_' + dimension + '_' + graph_suffix + '.png') 
    print('obs_max_distance_' + dimension + '_' + graph_suffix + ' creado')
    
    # OBSERVABLE MAX CANTIDAD CELDAS VIVAS VS INPUT
    plt.figure(figsize=(10, 6))
    plt.title('Maxima cantidad de celdas vivas por Input')
    plt.errorbar(x_values, avg_alive_cells_scalars[system], yerr=std_alive_cells_scalars[system], fmt='o')
    plt.xlabel('Input (%)')
    plt.ylabel('Maxima cantidad de celdas vivas')
    plt.xticks(x_values, percentages)
    plt.grid()
    
    plt.savefig('../images/' + dimension + '/obs_max_alive_cells_' +  dimension + '_' + graph_suffix + '.png') 
    print('obs_max_alive_cells_' + dimension + '_' + graph_suffix + ' creado')