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

    return list(x)

def convex_quadrature_steepest_descent_minimizer( f_conv_quad: callable, Q:list[list[float]], c:list[float], x_vec: list[float] , EPS = 1e-9, ITMAX = 25, verbose = True) -> list[float]:
    # f_conv_quad is the function to be minimized (needs to be convex quadrature)
    # Q is the matrix of the quadratic form
    # c is the vector of the linear form
    # EPS is the absolute error tolerance of the gradient norm
    # ITMAX is the maximum number of iterations
    # verbose is a boolean that determines whether or not to print the iterations

    print("\nexecution of convex quadrature steepest descent")

    Q_np = np.array(Q)
    x_vec_np = np.array(x_vec)

    eigenvalues, eigenvectors = np.linalg.eig(Q_np)
    is_definite = True
    for eigenvalue in eigenvalues:
        if eigenvalue < 0:
            print("Q is not positive definite and therefore f_conv_quad is not convex")
            raise Exception("Q is not positive definite and therefore f_conv_quad is not convex")
        elif eigenvalue == 0:
            is_definite = False

    if(verbose): print(f"All eigenvalues ({eigenvalues}) of Q are nonnegative (definite = {is_definite}) , therefore f_conv_quad is convex")

    #===================#
    #f(x)= 1/2 * x^T * Q * x + c^T * x + d
    #steepest descent: x_i+1 = x_i - alfa_i * GRAD(f(x_i))
    #g_i = Q*x_i + c
    #alfa_i = (g_i^T*g_i)/(g_i^T)

    iteration_counter = 0
    while iteration_counter < ITMAX:
        g_i = Q_np @ x_vec + c
        norm_g_i = np.linalg.norm(g_i)
        
        if(verbose): print("    iteration: ", iteration_counter, " position: ", x_vec, " function value: ", f_conv_quad(x_vec), " gradient norm: ", norm_g_i)
        if norm_g_i < EPS:
            if(verbose): print("convex quadrature steepest descent reached a global minimum (gradient norm < EPS): ", x_vec)
            return list(x_vec)
        
        alfa_i = (g_i.T @ g_i)/(g_i.T @ Q_np @ g_i)
        x_vec = x_vec - alfa_i * g_i

        print("    new position: ", x_vec, " alfa_i: ", alfa_i, " gradient norm: ", norm_g_i,"\n")

        iteration_counter += 1

    if(verbose): print("convex quadrature steepest descent reached a global minimum (iteration): ", x_vec)
    return list(x_vec)



