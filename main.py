import nonlinear_solvers 


def root_2(x):
    return x**2 - 2

r = nonlinear_solvers.bisection_method(f=root_2, ABSOLUTE_Y_ERROR= 1e-6, left_x=0, right_x=2, verbose=True)
r = nonlinear_solvers.false_position_method(f=root_2, ABSOLUTE_Y_ERROR= 1e-6, left_x=0, right_x=2, verbose=True)