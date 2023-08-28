import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
from matplotlib.colors import ListedColormap
from matplotlib.colors import LinearSegmentedColormap


#inputs = [1.0, 0.85, 0.70]
#inputs = [0.55, 0.40, 0.25]
inputs = [0.50, 0.50]
files = ['CONWAY', 'VONNEUMANN']

##### Graphics #####
img_plot = None
ax2d = None
max_distances_mat = []
alives_mat = []


def update(frame):
    
    global img_plot, ax2d, max_distances, alives
    
    max_distance_to_center = 0
    alive = 0
    line = lines[5 + frame*2]
    for z in range(sizez):
        for y in range(sizey):
            for x in range(sizex):
                number = int(line[x + sizex * y + sizex * sizey * z])
                if number == 1:
                    distance_to_center = np.sqrt((x - sizex/2)**2 + (y - sizey/2)**2)
                    if distance_to_center > max_distance_to_center:
                        max_distance_to_center = distance_to_center
                    alive += 1
                    normalized_distance = distance_to_center / max(sizex, sizey)
                    color = np.array([1, normalized_distance, max(0, normalized_distance/2)])
                    colored_grids[frame][x][y] = color
    
    if frame == 0:
        img_plot = ax2d.imshow(colored_grids[frame], interpolation='nearest')
    img_plot.set_array(colored_grids[frame])
    ax2d.set_title(f'Step {frame}', y=0.97, x=0.97)

    max_distances = np.append(max_distances, max_distance_to_center)
    alives = np.append(alives, alive)

    return img_plot
    
def graphics(input):
    global img_plot, ax2d
    fig, ax2d = plt.subplots(figsize=(10, 10))
    fig.canvas.manager.set_window_title('Game of Life')
    ax2d.set_xticks([])
    ax2d.set_yticks([])
    
    ani = FuncAnimation(fig, frames=max_step, func=update, interval=150)
    plt.tight_layout()
    ani.save('../gif/animation2d-colored_' + str(input) + '.gif')
    print("Gif 2d creado")
    return ani



for elem in files:
    #elem = round(elem*100)
    #with open('../output_' + str(elem) +'.txt', 'r') as file:
    #with open('../outputs/2Doutput_' + str(elem) + '.txt', 'r') as file:
    with open('../outputs/2D' + elem + 'output_50.txt', 'r') as file:
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
    
    graphics(elem)

    max_distances_mat.append(max_distances)
    alives_mat.append(alives)

plt.plot([1,2])
plt.show()

for i in range(len(alives_mat)):
    timeSteps = np.linspace(0, len(alives_mat[i]) - 2, len(alives_mat[i]) - 1)
    #plt.plot(timeSteps, alives_mat[i][1:], label=(str(round(inputs[i] * 100)) + '%'))
    plt.plot(timeSteps, alives_mat[i][1:], label=(files[i] + '%'))
    #plt.plot(timeSteps, alives_mat[i][1:]/(alives_mat[i][0]/inputs[i]), label = (str(round(inputs[i]*100)) + '%'))



plt.title('Celdas vivas en 2D')
plt.grid()
plt.xlabel('Pasos de tiempo')
plt.ylabel('Celdas vivas')
plt.legend()
plt.show()


for i in range(len(max_distances_mat)):
    timeSteps = np.linspace(0, len(max_distances_mat[i]) - 2, len(max_distances_mat[i]) - 1)
    #plt.plot(timeSteps, max_distances_mat[i][1:], label=(str(round(inputs[i] * 100)) + '%'))
    plt.plot(timeSteps, max_distances_mat[i][1:], label=(files[i] + '%'))


plt.title('El "radio" del patró 2D')
plt.grid()
plt.xlabel('Pasos de tiempo')
plt.ylabel('"Radio" [-]')
plt.legend()
plt.show()