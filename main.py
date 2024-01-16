import nonlinear_solvers 


def root_2(x):
    return x**2 - 2

r = nonlinear_solvers.bisection_method(f=root_2, ABSOLUTE_Y_ERROR= 1e-15, left_x=1, right_x=1.5, verbose=True)
r = nonlinear_solvers.false_position_method(f=root_2, ABSOLUTE_Y_ERROR= 1e-15, left_x=1, right_x=1.5, verbose=True)
r = nonlinear_solvers.secant_method(f=root_2, ABSOLUTE_Y_ERROR= 1e-15, x_0=1, x_1=1.5, verbose=True)