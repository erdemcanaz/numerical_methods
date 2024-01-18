import numpy as np

def least_square_linear_equation_solver(A: list[list[float]], b:list[float], verbose = True) -> list[float]:
    # Ax = b
    # min ||Ax - b||^2 = (Ax - b)^T * (Ax - b)

    if(verbose):
        print("\nexecution of least square linear equation solver")
        print(" A: ", A)
        print(" b: ", b)

    A_np = np.array(A)
    b_np = np.array(b)

    x_solution = np.linalg.inv(A_np.T @ A_np) @ A_np.T @ b_np

    if(verbose):
        print(" ||Ax - b||^2: ", np.linalg.norm(A_np @ x_solution - b_np))
        print("x_solution: ", x_solution)

    return list(x_solution)




