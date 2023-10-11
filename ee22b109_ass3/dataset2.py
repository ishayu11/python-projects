import numpy as np
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt

def func(x, A0, A1, A2, A3):
    yn = []
    for j in x:
        yn.append(A0 + A1*np.sin(T[0]*j) + A2*np.sin(T[1]*j) + A3*np.sin(T[2]*j))
    return yn

x = []
y = []

with open('dataset2.txt', 'r') as file:
    for line in file:
        line = line.strip()
        line = line.split()
        x.append(float(line[0]))
        y.append(float(line[1]))

# finding time period
min_index = 0
maxm = max(y)
temp1 = 100
for i in range(len(y)):
    if y[i] != maxm:
        temp2 = maxm + y[i]
        if temp2 < temp1:
            temp1 = temp2
            min_index = i

t1 = abs(x[min_index] - x[y.index(max(y))])
t1 *= 2

T = [2*np.pi/t1, 2*np.pi*3/t1, 2*np.pi*5/t1]
T0, T1, T2 = [], [], []
for i in x:
    T0.append(T[0] * i)
    T1.append(T[1] * i)
    T2.append(T[2] * i)

# Use column_stack to put the vectors side by side
M = np.column_stack([np.ones(len(x)), np.sin(T0), np.sin(T1), np.sin(T2)])

# Use the lstsq function to solve for p_1 and p_2
(A0, A1, A2, A3), _, _, _ = np.linalg.lstsq(M, y, rcond=None)
print(f"The estimated equation using least-squares is {A0} + {A1} sin({T[0]}x) + {A2} sin({T[1]}x) + {A3} sin({T[2]}x)")

assumptions = (A0, 6,2,1)
(a0, a1, a2, a3), _ = curve_fit(func, x, y, assumptions)
print(f"The estimated equation using curve_fit is {a0} + {a1} sin({T[0]}x) + {a2} sin({T[1]}x) + {a3} sin({T[2]}x)")

ylstsq = func(x, A0, A1, A2, A3)
y_estimated = func(x, a0, a1, a2, a3)


plt.title('Dataset 2')
plt.xscale('linear')
plt.yscale('linear')
plt.plot(x, y, color='cyan', label='Noisy', linewidth=1.0)
plt.plot(x, ylstsq, color='green', label='Least Squares')
plt.plot(x, y_estimated, color='red', label='Curve Fit')
plt.legend()
plt.grid(True)
plt.savefig("image2.jpg")