import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap


with open('../output.txt', 'r') as file:
    lines = file.readlines()

# Obtener los valores de max_step, time, sizex, sizey y sizez
max_step = int(lines[-1].split()[1])
time = int(lines[-2].split()[1])
sizex = int(lines[0].split()[1])
sizey = int(lines[1].split()[1])
sizez = int(lines[2].split()[1])

colored_grids = np.ones((max_step + 1, sizex, sizey, 3))
##### Graphics #####
img_plot = None
ax2d = None

def update(frame):
    global img_plot, ax2d
    line = lines[5 + frame*2]
    for z in range(sizez):
        for y in range(sizey):
            for x in range(sizex):
                number = int(line[x + sizex * y + sizex * sizey * z])
                if number == 1:
                    distance_to_center = np.sqrt((x - sizex/2)**2 + (y - sizey/2)**2)
                    normalized_distance = distance_to_center / max(sizex, sizey)
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
    
    ani = FuncAnimation(fig, frames=max_step, func=update, interval=100)
    plt.tight_layout()
    ani.save('../gif/animation2d-colored.gif')
    print("Gif 2d creado")
    return ani

graphics()