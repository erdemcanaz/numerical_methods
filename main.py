import nonlinear_solvers 


root_3_2 = lambda x: x**3 - 2
root_3_2_prime = lambda x: 3*(x**2)

r = nonlinear_solvers.bisection_method(f=root_3_2, ABSOLUTE_Y_ERROR= 1e-9, left_x=-10, right_x=10, verbose=True)
r = nonlinear_solvers.false_position_method(f=root_3_2, ABSOLUTE_Y_ERROR= 1e-9, left_x=-10, right_x=10, verbose=True)
r = nonlinear_solvers.secant_method(f=root_3_2, ABSOLUTE_Y_ERROR= 1e-9, x_0=-10, x_1=-9.5, verbose=True)
r = nonlinear_solvers.newton_raphson_method(f=root_3_2, f_prime=root_3_2_prime, ABSOLUTE_Y_ERROR= 1e-9, x_0=-10, verbose=True)
r = nonlinear_solvers.mullers_method(f=root_3_2, ABSOLUTE_Y_ERROR= 1e-9, x_0=-5, x_1=1, x_2=5, verbose=True)
