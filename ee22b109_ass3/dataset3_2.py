import numpy as np
from scipy.optimize import curve_fit
import scipy.constants as const
import matplotlib.pyplot as plt

def func(x, h, k ,c, T):
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


(h, k, c, T), _ = curve_fit(func, x, y, p0=(6.626e-34, 1.38e-23, 3e8, 5000))
print(f"The estimated temperature is {T}. ")
print(f"The estimated value of Boltzmann's constant is {k}. ")
print(f"The estimated value of Planck's constant is {h}. ")
print(f"The estimated value of speed of light is {c}. ")

# num = 2*h/(c**2)
# den = (h)/(k*T)
# print(f"Ratio of constants in the numerator is: {num}")
# print(f"Ratio of constants in the denominator is: {den}")

y_estimated = func(x, h, k, c, T)


plt.title('Dataset 3')
plt.xscale('linear')
plt.yscale('linear')
plt.plot(x, y, color='cyan', label='Noisy', linewidth=1.0)
plt.plot(x, y_estimated, color='red', label='Curve Fit')
plt.legend()
plt.grid(True)
plt.savefig("image3_2.jpg")