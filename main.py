import nonlinear_solvers 
import one_dimensional_search as ods

root_3_2 = lambda x: x**3 - 2
root_3_2_prime = lambda x: 3*(x**2)

# r = nonlinear_solvers.bisection_method(f=root_3_2, ABSOLUTE_Y_ERROR= 1e-9, left_x=-10, right_x=10, verbose=True)
# r = nonlinear_solvers.false_position_method(f=root_3_2, ABSOLUTE_Y_ERROR= 1e-9, left_x=-10, right_x=10, verbose=True)
# r = nonlinear_solvers.secant_method(f=root_3_2, ABSOLUTE_Y_ERROR= 1e-9, x_0=-10, x_1=-9.5, verbose=True)
# r = nonlinear_solvers.newton_raphson_method(f=root_3_2, f_prime=root_3_2_prime, ABSOLUTE_Y_ERROR= 1e-9, x_0=-10, verbose=True)
# r = nonlinear_solvers.mullers_method(f=root_3_2, ABSOLUTE_Y_ERROR= 1e-9, x_0=-5, x_1=1, x_2=5, verbose=True)

# For one dimensional search
f_1 = lambda x: (x**3)/3 -(x**2)/2 - x - 1
f_2 = lambda var_list: (var_list[0]**2) + 3*(var_list[1]**2) - 1

r = ods.dichotomous_search(f=f_1, interval=[1, 2], desired_interval_length=1e-6, EPS=1e-9, ITMAX=75, verbose=True)
r = ods.golden_section_search(f=f_1, interval=[1, 2], desired_interval_length=1e-6, ITMAX=75, verbose=True)
r = ods.fibonacci_search(f=f_1, interval=[1, 2], number_of_fibonacci_terms= 25, verbose=True)

r = ods.calculate_numeric_gradient(f=f_2, initial_position=[1, 2], dx= 1e-6)
