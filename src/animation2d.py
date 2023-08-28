import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap

##### Graphics #####
img_plot = None
ax2d = None
max_distances_mat = []
alives_mat = []

def update(frame):
    
    global img_plot, ax2d, max_distances, alives
    
    max_distance_to_center = 0
    alive_cells = 0
    line = lines[1 + frame*2]
    for z in range(size_z):
        for y in range(size_y):
            for x in range(size_x):
                number = int(line[x + size_x * y + size_x * size_y * z])
                if number == 1:
                    distance_to_center = np.sqrt((x - size_x/2)**2 + (y - size_y/2)**2)
                    if distance_to_center > max_distance_to_center:
                        max_distance_to_center = distance_to_center
                    alive_cells += 1
                    normalized_distance = distance_to_center / max(size_x, size_y)
                    color = np.array([1, normalized_distance, max(0, normalized_distance/2)])
                    colored_grids[frame][x][y] = color
    
    if frame == 0:
        img_plot = ax2d.imshow(colored_grids[frame], interpolation='nearest')
    img_plot.set_array(colored_grids[frame])
    ax2d.set_title(f'Step {frame}', y=0.97, x=0.97)

    max_distances = np.append(max_distances, max_distance_to_center)
    alives = np.append(alives, alive_cells)

    return img_plot
    
def graphics():
    global img_plot, ax2d
    fig, ax2d = plt.subplots(figsize=(10, 10))
    fig.canvas.manager.set_window_title('Game of Life')
    ax2d.set_xticks([])
    ax2d.set_yticks([])
    
    ani = FuncAnimation(fig, frames=max_step, func=update, interval=150)
    plt.tight_layout()
    ani.save('../gif/2d/animation_2d_' + file_suffix + '.gif')
    print('Gif 2d_' + file_suffix + ' creado')
    return ani


with open("../outputs/2d/data2d.txt", 'r') as data_file:
    data_lines = data_file.readlines()
    
for i in range(3): # 3 2d systems
    max_distances_mat = []
    alives_mat = []
    inputs = []  
    for j in range(6): # 6 inputs per system
        first_line = i*9*6 + j*9  # 6 inputs, each with 9 lines of data
        rule = str(data_lines[first_line].split()[1])
        ntype = str(data_lines[first_line+1].split()[1])
        radius = int(data_lines[first_line+2].split()[1])
        alive = int(data_lines[first_line+3].split()[1])
        max_step = int(data_lines[first_line+4].split()[1])
        size_x = int(data_lines[first_line+5].split()[1])
        size_y = int(data_lines[first_line+6].split()[1])
        size_z = int(data_lines[first_line+7] .split()[1])
        inputs = np.append(inputs, alive)
        
        file_suffix = rule + '_' + ntype + '_' + 'r' + str(radius) + '_' + str(alive)
        graphs_suffix = rule + '_' + ntype + '_' + 'r' + str(radius)
        with open('../outputs/2d/output_2d_' + file_suffix + '.txt', 'r') as file:
            lines = file.readlines()
        
        elapsed_time = int(lines[-1].split()[1])

        colored_grids = np.ones((max_step + 1, size_x, size_y, 3))
        max_distances = np.array([])
        alives = np.array([])
        
        graphics()

        max_distances_mat.append(max_distances)
        alives_mat.append(alives)
    
    # DISTANCIA MAX vs TIEMPO
    plt.figure(figsize=(10, 6))
    plt.title('Distancia maxima en funcion del tiempo')
    for i, curve_values in enumerate(max_distances_mat):
        x_values = np.arange(1, len(curve_values) + 1)
        plt.plot(x_values, curve_values, label=f'{inputs[i]} %')
    
    plt.xlabel('Tiempo')
    plt.ylabel('Distancia al centro')
    plt.legend(loc='upper right')
    
    plt.savefig('../images/2d/d_max_vs_tiempo_' + graphs_suffix + '.png')    

    # CELDAS VIVAS vs TIEMPO
    plt.figure(figsize=(10, 6))
    plt.title('Celdas vivas funcion del tiempo')
    for i, curve_values in enumerate(alives_mat):
        x_values = np.arange(1, len(curve_values) + 1)
        plt.plot(x_values, curve_values, label=f'{inputs[i]} %')
    
    plt.xlabel('Tiempo')
    plt.ylabel('Celdas vivas')
    plt.legend(loc='upper right')
    plt.savefig('../images/2d/celdas_vivas_vs_tiempo_' + graphs_suffix + '.png')    
    
    
    # MAXIMO DISTANCIA MAX (Observable) vs TIEMPO
    ave_dist = np.array([])
    std_dev_dist = np.array([])
    endline = np.array(["\n"])

    for curve_values in max_distances_mat:
        obser_dist = np.diff(curve_values)
        ave_dist = np.append(ave_dist, "AVERAGE " +  str(round(np.mean(obser_dist), 2)))
        std_dev_dist = np.append(std_dev_dist, "STD " + str(round(np.std(obser_dist),2)))
    
    file_path_dis = "observable_distance_" + graphs_suffix + ".txt"

    with open(file_path_dis, "a") as file:
        np.savetxt(file_path_dis, ave_dist, fmt ='%s')
        np.savetxt(file_path_dis, std_dev_dist, fmt = '%s')
        np.savetxt(file_path_dis, endline, fmt = '%s')

    
    # PENDIENTE CELDAS VIVAS (Observable) vs TIEMPO
    ave_alive = np.array([])
    std_dev_alive = np.array([])

    for curve_values in alives_mat:
        obser_alive = np.diff(curve_values)
        ave_alive = np.append(ave_alive, "AVERAGE " +  str(round(np.mean(obser_alive), 2)))
        std_dev_alive = np.append(std_dev_alive, "STD " + str(round(np.std(obser_alive),2)))
    
    file_path_alive = "observable_alive_" + graphs_suffix + ".txt"

    with open(file_path_alive, "a") as file:
        np.savetxt(file_path_alive, ave_dist, fmt ='%s')
        np.savetxt(file_path_alive, std_dev_dist, fmt = '%s')
        np.savetxt(file_path_alive, endline, fmt = '%s')

    
    # MAXIMO DISTANCIA MAX (Observable) vs INPUT
    
    # PENDIENTE CELDAS VIVAS (Observable) vs INPUT
    