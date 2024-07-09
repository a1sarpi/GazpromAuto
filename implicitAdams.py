# Невная схема
import math
import numpy as np
from matplotlib import pyplot as plt

from progon import *
from print_utils import *

# ДАНО
N = 12
n = 61

h1 = 0.05
tau1 = 0.05

h2 = 0.05
tau2 = 0.005

D = 1 / 4.

alpha = 64 - n
beta = N / 2

time_points = [0.5, 1.0]


@np.vectorize
def func(t, x):
    return np.cos(np.pi * t / 2) * (-18 * x ** 2 + 18 * x) - 12 * t + 12


np.set_printoptions(suppress=True)

rhs_lambda = lambda t, x: beta / 2 * (
        alpha * np.cos(np.pi * t / 2) - alpha * np.pi * (x - x ** 2) * np.sin(np.pi * t / 2) - 4)

analytic_solution_lambda = lambda t, x: alpha * beta * x * (1 - x) * np.cos(np.pi * t / 2) + 2 * beta * (1 - t)


def get_initial_vector(D, net_x):
    return 0


def get_left_boundary(t):
    return 0


def get_right_boundary(t):
    return 0


def assemble_implicit_matrix(D, h, tau):
    len_net = math.ceil(1 / h) + 1
    p = - D * tau / (h ** 2)
    q = 1 - 2 * p
    r = p
    A = np.array([[0] * len_net] +
                 [[0] * i + [p, q, r] + [0] * (len_net - i - 3) for i in range(len_net - 2)]
                 + [[0] * len_net])
    A[0][0] = 1
    A[-1][-1] = 1
    return A


def solve_with_implicit(D, h, tau):
    net_x_len = math.ceil(1 / h) + 1
    net_t_len = math.ceil(1 / tau) + 1
    net_x = np.array([i * h for i in range(net_x_len)])
    net_t = np.array([i * tau for i in range(net_t_len)])

    print(f"{net_x = }")
    print(f"{net_t = }")

    A = assemble_implicit_matrix(D, h, tau)
    print_matrix(A)

    sol = np.zeros((net_t_len, net_x_len))
    sol[0] = get_initial_vector(D, net_x)

    for i in range(1, net_t_len):
        beta_i = np.array([get_left_boundary(net_t[i])] +
                          [0] * (net_x_len - 2) +
                          [get_right_boundary(net_t[i])])
        beta_im1 = np.array([get_left_boundary(net_t[i - 1])] +
                            [0] * (net_x_len - 2) +
                            [get_right_boundary(net_t[i - 1])])
        f_i = np.array([0] + list(rhs_lambda(net_t[i], net_x[1:-1])) + [0])
        rhs_1 = tau * f_i + beta_i - beta_im1 + sol[i - 1]
        sol[i] = solve_progon(A, rhs_1)

    print("sol: ")
    print_matrix(sol, lambda x: round(x, 3))

    return sol


def implicit_analize(h, tau, filename="plot_2.png"):
    net_x_len = math.ceil(1 / h) + 1
    net_t_len = math.ceil(1 / tau) + 1
    net_x = np.array([i * h for i in range(net_x_len)])
    net_t = np.array([i * tau for i in range(net_t_len)])

    sol1 = solve_with_implicit(D, h, tau)
    sol_anal1 = np.matrix(func(time_points[0], net_x))
    sol_anal2 = np.matrix(func(time_points[1], net_x))
    sol1_1 = sol1[10]
    sol1_2 = sol1[len(sol1) - 1]
    dif_1 = np.max(np.abs(sol1_1 - sol_anal1))
    dif_2 = np.max(np.abs(sol1_2 - sol_anal2))
    print(f"{dif_1 = }")
    print(f"{dif_2 = }")

    fig, axs = plt.subplots(1, 2)
    for t in time_points:
        ax = axs[time_points.index(t)]

        analytic_sol1 = analytic_solution_lambda(t, net_x)
        index = math.ceil(t / tau)
        ax.plot(net_x, sol1[index], color='green')
        ax.plot(net_x, analytic_sol1, color='purple')
        ax.set_title('$t =%s$' % t)
    fig.savefig(filename, bbox_inches="tight")
    plt.close(fig)
