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

colored_grids = np.ones((max_step + 1, sizex, sizey, sizez, 3))
##### Graphics #####
fig = plt.figure(figsize=(10, 10))
fig.canvas.manager.set_window_title('Game of Life 3D')
ax3d = fig.add_subplot(111, projection='3d')
ax3d.set_xticks([])
ax3d.set_yticks([])
ax3d.set_zticks([])
ax3d.grid(False)


def update(frame):
    global ax3d
    ax3d.clear()
    ax3d.set_title(f'Step {frame}')
    ax3d.set_xlabel('X')
    ax3d.set_ylabel('Y')
    ax3d.set_zlabel('Z')
    ax3d.set_xlim(0, sizex)
    ax3d.set_ylim(0, sizey)
    ax3d.set_zlim(0, sizez)

    for z in range(sizez):
        for y in range(sizey):
            for x in range(sizex):
                number = int(lines[5 + frame*2][x + sizex * y + sizex * sizey * z])
                if number == 1:
                    distance_to_center = np.sqrt((x - sizex/2)**2 + (y - sizey/2)**2 + (z - sizez/2)**2)
                    normalized_distance = distance_to_center / max(sizex, sizey, sizez)
                    color = np.array([1, normalized_distance, max(0, normalized_distance/2)])
                    ax3d.scatter(x, y, z, c=[color], marker='o')

def graphics_3d():
    global ax3d
    ani = FuncAnimation(fig, frames=max_step, func=update, interval=150)
    ani.save('../gif/animation3d-colored.gif', writer='imagemagick')
    print("Gif 3d creado")
    return ani

graphics_3d()