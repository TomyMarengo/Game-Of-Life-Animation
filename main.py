import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

# Función para cargar los datos del archivo de salida de Java
def load_grid(filename):
    grid = []
    with open(filename, 'r') as file:
        for line in file:
            if line.strip() == "":
                continue
            values = [int(x) for x in line.strip().split()]
            grid.append(values)
    return np.array(grid)

# Función para actualizar la visualización en cada paso de tiempo
def update(frame):
    ax.clear()
    ax.imshow(grid_frames[frame], cmap='binary', interpolation='nearest', aspect='auto')
    ax.set_title(f'Step {frame}')

filename = 'output.txt'  # Cambia esto al nombre de tu archivo de salida de Java
grid_data = load_grid(filename)

# Convierte los datos en una lista de matrices para cada paso de tiempo
grid_frames = [grid_data[i:i+10] for i in range(0, len(grid_data), 10)]

fig, ax = plt.subplots()
ani = animation.FuncAnimation(fig, update, frames=len(grid_frames), interval=500)
plt.show()