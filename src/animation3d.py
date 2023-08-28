import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap

#inputs = [1.0, 0.85, 0.70]
#inputs = [0.55, 0.40, 0.25]
inputs = [0.55]

max_distances_mat = []
alives_mat = []

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

    max_distance_to_center = 0
    alive = 0

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

                    if distance_to_center > max_distance_to_center:
                        max_distance_to_center = distance_to_center
                    alive += 1

    max_distances = np.append(max_distances, max_distance_to_center)
    alives = np.append(alives, alive)

def graphics_3d(input):
    global ax3d
    ani = FuncAnimation(fig, frames=max_step, func=update, interval=150)
    ani.save('../gif/animation3d-colored' + str(input) + '.gif', writer='imagemagick') #--> my computer STRUGGELS to finish to run this animation, it seems to takes ages
    print("Gif 3d creado")
    return ani



for elem in inputs:
    elem = round(elem * 100)
    with open('../output_' + str(elem) + '.txt', 'r') as file:
        lines = file.readlines()

    # Obtener los valores de max_step, time, sizex, sizey y sizez
    alive = int(lines[-1].split()[1])
    max_step = int(lines[-2].split()[1])
    time = int(lines[-3].split()[1])
    sizex = int(lines[0].split()[1])
    sizey = int(lines[1].split()[1])
    sizez = int(lines[2].split()[1])

    colored_grids = np.ones((max_step + 1, sizex, sizey, 3))

    max_distances = np.array([])
    alives = np.array([])

    graphics_3d(elem)

    max_distances_mat.append(max_distances)
    alives_mat.append(alives)

plt.plot([1,2,3])
plt.show()

for i in range(len(alives_mat)):
    timeSteps = np.linspace(0, len(alives_mat[i]) - 2, len(alives_mat[i]) - 1)
    plt.plot(timeSteps, alives_mat[i][1:], label=(str(round(inputs[i] * 100)) + '%'))
    # plt.plot(timeSteps, alives_mat[i][1:]/(alives_mat[i][0]/inputs[i]), label = (str(round(inputs[i]*100)) + '%'))

plt.title('Celdas vivas en 3D')
plt.grid()
plt.xlabel('Pasos de tiempo')
plt.ylabel('Celdas vivas')
plt.legend()
plt.show()




for i in range(len(max_distances_mat)):
    timeSteps = np.linspace(0, len(max_distances_mat[i]) - 2, len(max_distances_mat[i]) - 1)
    plt.plot(timeSteps, max_distances_mat[i][1:], label=(str(round(inputs[i] * 100)) + '%'))


plt.title('El "radio" del patró 3D')
plt.grid()
plt.xlabel('Pasos de tiempo')
plt.ylabel('"Radio" [-]')
plt.legend()
plt.show()
