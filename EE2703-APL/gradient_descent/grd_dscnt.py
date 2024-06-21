import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def quad_func(x):
    return x ** 2 + 3 * x + 8

def quad_deriv(x):
    return 2 * x + 3

def cubic_func(x, y):
    return x ** 4 - 16 * x ** 3 + 96 * x ** 2 - 256 * x + y ** 2 - 4 * y + 262

def cubic_deriv_x(x, y):
    return 4 * x ** 3 - 48 * x ** 2 + 192 * x - 256

def cubic_deriv_y(x, y):
    return 2 * y - 4

def gaussian_func(x, y):
    return np.exp(-(x - y) ** 2) * np.sin(y)

def gaussian_deriv_x(x, y):
    return -2 * np.exp(-(x - y) ** 2) * np.sin(y) * (x - y)

def gaussian_deriv_y(x, y):
    return np.exp(-(x - y) ** 2) * np.cos(y) + 2 * np.exp(-(x - y) ** 2) * np.sin(y) * (x - y)

def trig_func(x):
    return np.cos(x) ** 4 - np.sin(x) ** 3 - 4 * np.sin(x) ** 2 + np.cos(x) + 1

def trig_deriv(x):
    return -4 * np.sin(x) * (np.cos(x) ** 3) - 3 * (np.sin(x) ** 2) * np.cos(x) - 8 * np.sin(x) * np.cos(x) - np.sin(x)

def oneD_grad_desc(function, derivative, limit, vid):
    x_base = np.linspace(limit[0], limit[1], 200)
    y_base = function(x_base)
    best_x = 3
    best_cost = function(best_x)
    fig, ax = plt.subplots()
    ax.plot(x_base, y_base)
    x_all, y_all = [], []
    ln_all, = ax.plot([], [], 'ro', markersize=4)
    ln_good, = ax.plot([], [], 'go', markersize=7)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    learning_rate = 0.15

    def one_step_deriv(frame):
        nonlocal best_x, learning_rate
        x_all.append(best_x)
        y_all.append(function(best_x))
        x = best_x - derivative(best_x) * learning_rate
        best_x = x
        y = function(x)
        ln_good.set_data(x, y)
        ln_all.set_data(x_all, y_all)
        if frame == 49:
            print(f"Best x:{x}", f"Best y:{y}")

    anim = FuncAnimation(fig, one_step_deriv, frames=range(50), interval=500, repeat=False)
    anim.save(vid, writer='pillow', dpi=100)
    plt.show()

def twoD_grad_desc(function, derivative_x, derivative_y, x_interval, y_interval, learning_rate, vid, best_x=0, best_y=0):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")
    X = np.arange(x_interval[0], x_interval[1], 0.2)
    Y = np.arange(y_interval[0], y_interval[1], 0.2)
    X, Y = np.meshgrid(X, Y)
    Z = function(X, Y)
    surf = ax.plot_surface(X, Y, Z, cmap="viridis", alpha=0.8)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")

    # stores points that are generated while performing gradient descent.
    x_all, y_all, z_all = [], [], []
    ln_all, = ax.plot([], [], [], 'ro', markersize=4)
    ln_good, = ax.plot([], [], [], 'go', markersize=7)

    best_cost = function(best_x, best_y)

    def one_step_deriv(frame):
        nonlocal best_x, best_y, best_cost
        x_all.append(best_x)
        y_all.append(best_y)
        z_all.append(function(best_x, best_y))

        new_x = best_x - derivative_x(best_x, best_y) * learning_rate
        new_y = best_y - derivative_y(best_x, best_y) * learning_rate

        new_cost = function(new_x, new_y)

        # updating x and y if the new cost is better
        if new_cost < best_cost:
            best_x = new_x
            best_y = new_y
            best_cost = new_cost

        ln_good.set_data([best_x], [best_y])
        ln_good.set_3d_properties([best_cost])
        ln_all.set_data(x_all, y_all)
        ln_all.set_3d_properties(z_all)

        if frame == 79:
            print("best x = ", best_x, "best y = ",best_y, "best z = ",function(best_x, best_y))

    anim = FuncAnimation(fig, one_step_deriv, frames=range(80), interval=8, repeat=False)
    anim.save(vid, writer='pillow', dpi=100)
    plt.show()


oneD_grad_desc(quad_func, quad_deriv, [-5, 5], "a1.gif")
oneD_grad_desc(trig_func, trig_deriv, [0, 2 * np.pi], "a4.gif")

twoD_grad_desc(cubic_func, cubic_deriv_x, cubic_deriv_y, [-10, 10], [-10, 10], 0.1, "a2.gif", 2, 0)
twoD_grad_desc(gaussian_func, gaussian_deriv_x, gaussian_deriv_y, [-np.pi, np.pi], [-np.pi, np.pi], 0.05, "a3.gif", -1, -1)
