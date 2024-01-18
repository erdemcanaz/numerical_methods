import numpy as np

def convex_quadrature_direct_solver(f_conv_quad: callable, Q:list[list[float]], c:list[float],  verbose = True) -> list[float]:
    # f_conv_quad is the function to be minimized (needs to be convex quadrature)
    # Q is the matrix of the quadratic form
    # verbose is a boolean that determines whether or not to print the iterations

    print("\nexecution of convex quadrature direct solver")
    Q_np = np.array(Q)
    eigenvalues, eigenvectors = np.linalg.eig(Q_np)

    is_definite = True
    for eigenvalue in eigenvalues:
        if eigenvalue < 0:
            print("Q is not positive definite and therefore f_conv_quad is not convex")
            raise Exception("Q is not positive definite and therefore f_conv_quad is not convex")
        elif eigenvalue == 0:
            is_definite = False

    if(verbose): print(f"All eigenvalues ({eigenvalues}) of Q are nonnegative (definite = {is_definite}) , therefore f_conv_quad is convex")

    #f(x)= 1/2 * x^T * Q * x + c^T * x + d
    #f'(x)= Q * x + c
    #set f'(x) = 0 --> (Q * x + c) = 0 -> x = -Q^-1 * c        
    Q_inverse_np = np.linalg.inv(Q_np)
    x = (-1)*Q_inverse_np @ c

    if(verbose):
        print("x*: ", x)
        print("f(x*): ", f_conv_quad(x))

    return x





