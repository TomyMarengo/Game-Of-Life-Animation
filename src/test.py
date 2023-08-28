import matplotlib.pyplot as plt
import numpy as np


list = [343, 343, 68, 384, 344, 548, 776, 896, 1020, 1084, 1608, 1912, 2412, 2704, 2948, 3652, 3884, 4836]



my_array = np.array([])  # Create an empty array

# Add items to the array
item1 = 5
item2 = 10
item3 = 15

my_array = np.append(my_array, item1)
my_array = np.append(my_array, item2)
my_array = np.append(my_array, item3)

print(my_array)

plt.show()