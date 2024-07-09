import numpy as np
from print_utils import *

def solve_progon(matrixA, vecB, silent=True):
    N = matrixA.shape[0]
    a_i = np.zeros(N)
    b_i = np.zeros(N)
    c_i = np.zeros(N)
    a_i[0] = 0
    b_i[0] = matrixA[0][0]
    c_i[0] = matrixA[0][1]
    c_i[-1] = 0
    a_i[-1] = matrixA[-1][-2]
    b_i[-1] = matrixA[-1][-1]
    for i in range(1, N-1):
        a_i[i] = matrixA[i][i-1]
        b_i[i] = matrixA[i][i]
        c_i[i] = matrixA[i][i+1]
    if not silent:
        print('\na_i, b_i, c_i:')
        print_matrix(a_i, rounding_way=lambda x: round(x, 2))
        print_matrix(b_i, rounding_way=lambda x: round(x, 2))
        print_matrix(c_i, rounding_way=lambda x: round(x, 2))

    L = np.zeros(N)
    M = np.zeros(N)
    L[0] = - c_i[0] / b_i[0]
    M[0] = vecB[0] / b_i[0]

    for i in range(1, N):
        L[i] = - c_i[i] / (L[i-1] * a_i[i] + b_i[i])
        M[i] = (vecB[i] - M[i-1] * a_i[i]) / (L[i-1] * a_i[i] + b_i[i])

    if not silent:
        print('\nL_i, M_i:')
        print_matrix(L, rounding_way=lambda x: round(x, 2))
        print_matrix(M, rounding_way=lambda x: round(x, 2))

    sol_x = np.zeros(N)
    sol_x[-1] = M[-1]
    for i in range(-1, -N-1, -1):
        sol_x[i] = L[i] * sol_x[i+1] + M[i]

    if not silent:
        print('\nSolution:')
        print_matrix(sol_x, rounding_way=lambda x: round(x, 4))

        print('\nSolution with numpy:')
        print_matrix(np.linalg.solve(matrixA, vecB), rounding_way=lambda x: round(x, 2))

    return sol_x
