import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap

##### Graphics #####
img_plot = None
ax2d = None

def update(frame):
    global img_plot, ax2d, max_distances, alives
    
    line = lines[1 + frame*2]
    for z in range(size_z):
        for y in range(size_y):
            for x in range(size_x):
                number = int(line[x + size_x * y + size_x * size_y * z])
                if number == 1:
                    distance_to_center = np.sqrt((x - size_x/2)**2 + (y - size_y/2)**2)
                    normalized_distance = distance_to_center / max(size_x, size_y)
                    color = np.array([1, normalized_distance, max(0, normalized_distance/2)])
                    colored_grids[frame][x][y] = color
    
    if frame == 0:
        img_plot = ax2d.imshow(colored_grids[frame], interpolation='nearest')
    img_plot.set_array(colored_grids[frame])
    ax2d.set_title(f'Step {frame}', y=0.97, x=0.97)

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
    
maxRep = 5
systems = 3
data_per_system = 9
percentages = [100, 85, 70, 55, 40, 25]
inputs = len(percentages)

for system in range(systems): # 3 2d systems
    for my_input in range(inputs): # 6 inputs per system
        first_line =  ( inputs * system + my_input ) * data_per_system * maxRep
        rule = str(data_lines[first_line].split()[1])
        ntype = str(data_lines[first_line+1].split()[1])
        radius = int(data_lines[first_line+2].split()[1])
        alive = int(data_lines[first_line+3].split()[1])
        max_step = int(data_lines[first_line+4].split()[1])
        size_x = int(data_lines[first_line+5].split()[1])
        size_y = int(data_lines[first_line+6].split()[1])
        size_z = int(data_lines[first_line+7] .split()[1])

        file_suffix = rule + '_' + ntype + '_' + 'r' + str(radius) + '_' + str(alive) + "_0"
        with open('../outputs/2d/output_2d_' + file_suffix + '.txt', 'r') as file:
            lines = file.readlines()
        
        colored_grids = np.ones((max_step + 1, size_x, size_y, 3))
        graphics()