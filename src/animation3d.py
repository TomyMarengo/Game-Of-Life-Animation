import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap

##### Graphics #####
fig = plt.figure(figsize=(10, 10))
fig.canvas.manager.set_window_title('Game of Life 3D')
ax3d = fig.add_subplot(111, projection='3d')
ax3d.set_xticks([])
ax3d.set_yticks([])
ax3d.set_zticks([])
ax3d.grid(False)


def update(frame):
    global ax3d, max_distances, alives
    ax3d.clear()
    ax3d.set_title(f'Step {frame}')
    ax3d.set_xlabel('X')
    ax3d.set_ylabel('Y')
    ax3d.set_zlabel('Z')
    ax3d.set_xlim(0, size_x)
    ax3d.set_ylim(0, size_y)
    ax3d.set_zlim(0, size_z)

    line = lines[1 + frame*2]
    for z in range(size_z):
        for y in range(size_y):
            for x in range(size_x):
                number = int(line[x + size_x * y + size_x * size_y * z])
                if number == 1:
                    distance_to_center = np.sqrt((x - size_x/2)**2 + (y - size_y/2)**2 + (z - size_z/2)**2)
                    normalized_distance = distance_to_center / max(size_x, size_y, size_z)
                    color = np.array([1, normalized_distance, max(0, normalized_distance/2)])
                    ax3d.scatter(x, y, z, c=[color], marker='o')

def graphics():
    global ax3d
    ani = FuncAnimation(fig, frames=max_step, func=update, interval=150)
    ani.save('../gif/3d/animation_3d_' + file_suffix + '.gif', writer='imagemagick') #--> my computer STRUGGELS to finish to run this animation, it seems to takes ages
    print('Gif 3d_' + file_suffix + ' creado')
    return ani

with open("../outputs/3d/data3d.txt", 'r') as data_file:
    data_lines = data_file.readlines()
    
maxRep = 5
systems = 3
data_per_system = 9
percentages = [100, 85, 70, 55, 40, 25]
inputs = len(percentages)

for system in range(systems): # 3 3d systems 
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
        with open('../outputs/3d/output_3d_' + file_suffix + '.txt', 'r') as file:
            lines = file.readlines()
        
        colored_grids = np.ones((max_step + 1, size_x, size_y, size_z, 3))
        graphics()