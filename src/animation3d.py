import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from mpl_toolkits.mplot3d import Axes3D

with open('../output.txt', 'r') as file:
    lines = file.readlines()

# Obtener los valores de maxstep, sizex, sizey y sizez
max_step = int(lines[0].split()[1])
sizex = int(lines[1].split()[1])
sizey = int(lines[2].split()[1])
sizez = int(lines[3].split()[1])

grids = [[[[0 for _ in range(sizez)] for _ in range(sizey)] for _ in range(sizex)] for _ in range(max_step + 1)]

j = -1
for i in range(6, len(lines), 2):
    j += 1
    for z in range(sizez):
        for y in range(sizey):
            for x in range(sizex):
                line = lines[i]
                grids[j][x][y][z] = int(line[x + sizex * y + sizex * sizey * z])

##### Graphics #####

def update(frame):
    global ax3d
    ax3d.clear()
    ax3d.set_title(f'Step {frame}')
    ax3d.set_xlabel('X')
    ax3d.set_ylabel('Y')
    ax3d.set_zlabel('Z')
    ax3d.set_xlim(0, sizex)
    ax3d.set_ylim(0, sizey)
    ax3d.set_zlim(-sizez*1.7, sizez*1.7)
    ax3d.set_xticks([])
    ax3d.set_yticks([])
    ax3d.set_zticks([])
    ax3d.grid(False)
    
    # Plot the 3D grid
    for z in range(sizez):
        for y in range(sizey):
            for x in range(sizex):
                if grids[frame][x][y][z] == 1:
                    ax3d.scatter(x, y, z, c='yellow', marker='s')

def graphics_3d():
    global ax3d
    fig = plt.figure(figsize=(10, 10))
    fig.canvas.manager.set_window_title('Game of Life 3D')
    ax3d = fig.add_subplot(111, projection='3d')

    ax3d.xaxis.set_pane_color((0.0, 0.8, 0.8, 0.5))
    ax3d.yaxis.set_pane_color((0.0, 0.8, 0.8, 0.5))
    ax3d.zaxis.set_pane_color((0.0, 0.8, 0.8, 0.5))
    ani = FuncAnimation(fig, frames=max_step, func=update, interval=100)
    ani.save('../gif/animation3d.gif', writer='imagemagick')
    plt.show()
    return ani

graphics_3d()