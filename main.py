import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

with open('output.txt', 'r') as file:
    lines = file.readlines()

# Obtener los valores de maxstep, sizex, sizey y sizez
max_step = int(lines[0].split()[1])
sizex = int(lines[1].split()[1])
sizey = int(lines[2].split()[1])
sizez = int(lines[3].split()[1])

grids = [[[[0 for _ in range(sizez)] for _ in range(sizey)] for _ in range(sizex)] for _ in range(max_step + 1)]

j = -1
for i in range(6, len(lines), 3):
    j += 1
    for z in range(sizez):
        for y in range(sizey):
            for x in range(sizex):
                line = lines[i]
                grids[j][x][y][z] = int(line[x + sizex * y + sizex * sizey * z])

##### Graphics #####

img_plot = None

def update(frame):
    global img_plot
    img_plot.set_data(grids[frame])
    return img_plot
    
def graphics():
    global img_plot
    fig, ax = plt.subplots(figsize=(10, 10))
    fig.canvas.manager.set_window_title('Game of Life')
    img_plot = ax.imshow(grids[0], interpolation='nearest', cmap=ListedColormap(['darkturquoise', 'yellow']))
    ax.set_xticks([])
    ax.set_yticks([])
    ani = FuncAnimation(fig, frames=max_step, func=update, interval=100)
    plt.tight_layout()
    ani.save('testconway.gif')
    plt.show()
    return ani

graphics()
