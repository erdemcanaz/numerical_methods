import nonlinear_solvers, one_dimensional_search, unconstrained_optimization, least_squares
import math

root_3_2 = lambda x: x**3 - 2
root_3_2_prime = lambda x: 3*(x**2)


# For nonlinear_solvers
r = nonlinear_solvers.bisection_method(f=root_3_2, ABSOLUTE_Y_ERROR= 1e-9, left_x=-10, right_x=10, verbose=True)
r = nonlinear_solvers.false_position_method(f=root_3_2, ABSOLUTE_Y_ERROR= 1e-9, left_x=-10, right_x=10, verbose=True)
r = nonlinear_solvers.secant_method(f=root_3_2, ABSOLUTE_Y_ERROR= 1e-9, x_0=-10, x_1=-9.5, verbose=True)
r = nonlinear_solvers.newton_raphson_method(f=root_3_2, f_prime=root_3_2_prime, ABSOLUTE_Y_ERROR= 1e-9, x_0=-10, verbose=True)
r = nonlinear_solvers.mullers_method(f=root_3_2, ABSOLUTE_Y_ERROR= 1e-9, x_0=-5, x_1=1, x_2=5, verbose=True)

# For one dimensional search
f_1 = lambda x: (x**3)/3 -(x**2)/2 - x - 1
f_2 = lambda var_list: (var_list[0]**2) + 3*(var_list[1]**2) - 1
f_3 = lambda var_list: (var_list[0]**2) + 2*(var_list[1]**2)

r = one_dimensional_search.dichotomous_search(f=f_1, interval=[1, 2], desired_interval_length=1e-6, EPS=1e-9, ITMAX=75, verbose=True)
r = one_dimensional_search.golden_section_search(f=f_1, interval=[1, 2], desired_interval_length=1e-6, ITMAX=75, verbose=True)
r = one_dimensional_search.fibonacci_search(f=f_1, interval=[1, 2], number_of_fibonacci_terms= 25, verbose=True)
r = one_dimensional_search.calculate_numeric_gradient(f=f_2, initial_position=[1, 2], dx= 1e-6)
r = one_dimensional_search.steepest_descent(f=f_3, initial_position=[1, 1], MAX_FUNCTION_CHANGE = 0.5, MAX_ALFA = 32, EPS = 1e-9, ITMAX = 75, verbose = True)

#for unconstrained optimization
Q=[[3,-1,-1],[-1,2,0],[-1,0,4]]
c = [1, -2, 3]
r = unconstrained_optimization.convex_quadrature_direct_solver(f_conv_quad= f_3, Q=Q, c=c, verbose=True)

Q = [[2,0],[0,4]]
c = [0,0]
r = unconstrained_optimization.convex_quadrature_steepest_descent_minimizer(f_conv_quad= f_3, Q=Q, c=c, x_vec=[1, 1], EPS = 1e-9, ITMAX = 25, verbose = True)


#for least squares
A = [ [2,3], [7,5], [2,4]]
b = [3.49, 7.60, 4.2]

r = least_squares.least_square_linear_equation_solver(A=A, b=b, verbose=True)