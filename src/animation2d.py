import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap

with open('../output.txt', 'r') as file:
    lines = file.readlines()

# Obtener los valores de maxstep, sizex, sizey y sizez
max_step = int(lines[0].split()[1])
sizex = int(lines[1].split()[1])
sizey = int(lines[2].split()[1])
sizez = int(lines[3].split()[1])

grids = [[[[0 for _ in range(1)] for _ in range(sizey)] for _ in range(sizex)] for _ in range(max_step + 1)]

j = -1
for i in range(6, len(lines), 2):
    j += 1
    for z in range(sizez):
        for y in range(sizey):
            for x in range(sizex):
                line = lines[i]
                grids[j][x][y][0] = int(line[x + sizex * y + sizex * sizey * z])

##### Graphics #####

img_plot = None
ax2d = None

def update(frame):
    global img_plot, ax2d
    img_plot.set_data(grids[frame])
    ax2d.set_title(f'Step {frame}', y=0.97, x=0.97)
    return img_plot
    
def graphics():
    global img_plot, ax2d
    fig, ax2d = plt.subplots(figsize=(10, 10))
    fig.canvas.manager.set_window_title('Game of Life')
    img_plot = ax2d.imshow(grids[0], interpolation='nearest', cmap=ListedColormap(['darkturquoise', 'yellow']))
    ax2d.set_xticks([])
    ax2d.set_yticks([])
    ani = FuncAnimation(fig, frames=max_step, func=update, interval=100)
    plt.tight_layout()
    ani.save('../gif/animation2d.gif')
    plt.show()
    return ani

graphics()