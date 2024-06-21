import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def stline(x, m, c):
    yn = []
    for j in x:
        yn.append(j*m+c)
    return yn

x = []
y = []

with open('dataset1.txt', 'r') as file:
    for line in file:
        line = line.strip()
        line = line.split()
        x.append(float(line[0]))
        y.append(float(line[1]))



# Use column_stack to put the vectors side by side
M = np.column_stack([x, np.ones(len(x))])

# Use the lstsq function to solve for p_1 and p_2
(p1, p2), _, _, _ = np.linalg.lstsq(M, y, rcond=None)
print(f"The estimated equation is {p1} x + {p2}")

yn = stline(x, p1, p2)

selected_x = x[::25]
selected_y = y[::25]


plt.title('Dataset 1')
plt.xscale('linear')
plt.yscale('linear')
plt.plot(x, y, color='green', label='Noisy', linewidth=1.0)
plt.scatter(selected_x, selected_y, marker='o', color='red', s=50, zorder = 2)
plt.plot(x, yn, color='cyan', label='Data Points')
plt.legend()
plt.grid(True)
plt.savefig("image1.jpg")