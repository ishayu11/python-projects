import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as const
import matplotlib.pyplot as plt

def func(x, T):
    h = const.Planck
    k = const.Boltzmann
    c = const.speed_of_light

    yn = []
    for j in x:
        numerator = 2*h*(j**3)/(c**2)
        denominator = (np.e**((h*j)/(k*T)))-1
        yn.append(numerator/denominator)
    return yn

x = []
y = []

with open('dataset3.txt', 'r') as file:
    for line in file:
        line = line.strip()
        line = line.split()
        x.append(float(line[0]))
        y.append(float(line[1]))


(T), _ = curve_fit(func, x, y, p0=5000)
print(f"The estimated temperature is {T}. ")

y_estimated = func(x, T)


plt.title('Dataset 3')
plt.xscale('linear')
plt.yscale('linear')
plt.plot(x, y, color='cyan', label='Noisy', linewidth=1.0)
plt.plot(x, y_estimated, color='red', label='Curve Fit')
plt.legend()
plt.grid(True)
plt.savefig("image3.jpg")