import math, copy, time

def calculate_numeric_gradient(f: callable, initial_position: list[float], dx= 1e-6) -> float:
    number_of_variables = len(initial_position)
    gradient = []

    position_for_ith_var = copy.deepcopy(initial_position)
    for i in range(number_of_variables):
        position_for_ith_var[i] += dx
        f_initial = f(initial_position)
        f_for_ith_var = f(position_for_ith_var)
        gradient.append((f_for_ith_var - f_initial)/dx)
        position_for_ith_var[i] -= dx    

    return gradient

def dichotomous_search(f = None, interval = None , desired_interval_length = 1e-6, EPS = 1e-9, ITMAX = 75, verbose = True) -> float:
    # f is the function to be minimized
    # interval is a list of two numbers, the left and right endpoints of the interval
    # desired_interval_length is the length of the interval that we want to achieve
    # EPS is the absolute error tolerance
    # ITMAX is the maximum number of iterations
    # verbose is a boolean that determines whether or not to print the iterations
    if(verbose): print("\nexecution of dichotomous search")

    iteration_counter = 0
    while iteration_counter < ITMAX:
        if(verbose): print("iteration: ", iteration_counter, " interval: ", interval)

        if abs(interval[1] - interval[0]) < desired_interval_length or iteration_counter >= ITMAX:
            return (interval[1]+interval[0])/2
        
        mid_point = (interval[0] + interval[1])/2
        x_left = mid_point - EPS/2
        x_right = mid_point + EPS/2
        if f(x_left) < f(x_right):
            interval[1] = x_right
        else:
            interval[0] = x_left
        pass

        iteration_counter += 1

def golden_section_search(f: callable , interval: list, desired_interval_length = 1e-6, ITMAX = 75, verbose = True) -> float:
    # <--a0-------b1-------a1-------b0-->
    # f is the function to be minimized
    # interval is a list of two numbers, the left and right endpoints of the interval
    # desired_interval_length is the length of the interval that we want to achieve
    # ITMAX is the maximum number of iterations
    # verbose is a boolean that determines whether or not to print the iterations
    if(verbose): print("\nexecution of golden section search")

    GOLDEN_RATIO = 0.61803398875 # (math.sqrt(5) - 1)/2    
    COMPLEMENTARY_GOLDEN_RATIO = 1 - GOLDEN_RATIO

    iteration_counter = 0
    interval_length = abs(interval[1] - interval[0])
    del_x = COMPLEMENTARY_GOLDEN_RATIO * interval_length
    a1 = interval[0] + del_x
    b1 = interval[1] - del_x

    while iteration_counter < ITMAX:
        y_a1 = f(a1)
        y_b1 = f(b1)

        if(y_a1 < y_b1): #ignore the interval (b1, b0)
            interval[1] = b1
            b1 = a1 # thanks to the golden ratio
            a1 = interval[0] + (interval[1] - b1)
        else: #ignore the interval (a0, a1)
            interval[0] = a1
            a1 = b1
            b1 = interval[1] - (a1 - interval[0])

        if(verbose): print("iteration: ", iteration_counter, " interval: ", interval)

        if abs(interval[1] - interval[0]) < desired_interval_length or iteration_counter >= ITMAX:
            return (interval[1]+interval[0])/2

        iteration_counter += 1

def fibonacci_search(f: callable, interval: list, number_of_fibonacci_terms: int, verbose = True) -> float:
    # f is the function to be minimized
    # interval is a list of two numbers, the left and right endpoints of the interval
    # number_of_fibonacci_terms is the number of fibonacci terms to be used
    # ITMAX is the maximum number of iterations
    # verbose is a boolean that determines whether or not to print the iterations

    if(verbose):
        print("\nexecution of fibonacci search")
        print("initial interval: ", interval)

    fibonacci_terms = [1, 2]
    initial_term = 1
    for i in range(number_of_fibonacci_terms-2):
        fibonacci_terms.append(fibonacci_terms[i] + fibonacci_terms[i+1])
    
    error = abs(interval[1] - interval[0])/fibonacci_terms[-1]

    for i in range(number_of_fibonacci_terms-2):
        number_of_sections = fibonacci_terms[-(i+1)]
        lenght_of_section = abs(interval[1] - interval[0])
        del_x = lenght_of_section/number_of_sections
        
        x_1 = interval[0]+ del_x * fibonacci_terms[-(i+3)]
        x_2 = interval[0]+ del_x * fibonacci_terms[-(i+2)]

        y_1 = f(x_1)
        y_2 = f(x_2)

        if(verbose): print("iteration: ", i+1, " interval: ", interval, " number of sections: ", number_of_sections)
        if y_1 < y_2:
            interval[1] = x_2
        else:
            interval[0] = x_1

    if(verbose): 
        print("final interval: ", interval)
        print("result: ", (interval[1]+interval[0])/2)
        print("error: ", error)

    return (interval[1]+interval[0])/2

def steepest_descent(f:callable, initial_position: list[float], MAX_FUNCTION_CHANGE = 1, MAX_ALFA = 32, EPS = 1e-9, ITMAX = 75, verbose = True) -> float:
    # f is the function to be minimized
    # initial_position is the initial guess of the minimum
    # MAX_FUNCTION_CHANGE is the maximum change in the function value after each iteration
    # MAX_ALFA is the maximum value of alfa (multiplication factor of the gradient)
    # EPS is the absolute error tolerance of the gradient norm
    # ITMAX is the maximum number of iterations
    # verbose is a boolean that determines whether or not to print the iterations

    if(verbose): print("\nexecution of steepest descent")

    iteration_counter = 0
    while iteration_counter < ITMAX:
        if(verbose): print("iteration: ", iteration_counter, " position: ", initial_position, " function value: ", f(initial_position))

        gradient = calculate_numeric_gradient(f=f, initial_position=initial_position, dx = EPS/10)
        gradient_norm = math.sqrt(sum([i**2 for i in gradient]))
        if gradient_norm < EPS:
            if(verbose): print("steepest descent reached a local minimum (gradient norm < EPS): ", initial_position)
            return initial_position
        
        alfa_i =  min(MAX_FUNCTION_CHANGE/gradient_norm, MAX_ALFA)

        while True:
            new_position = []
            for variable_index, position_variable in enumerate(initial_position):
                next_position_variable = position_variable - alfa_i*gradient[variable_index]
                new_position.append(next_position_variable)

            if f(new_position) < f(initial_position):
                initial_position = new_position
                break
        
            print("     alfa_i: ", alfa_i, "gradient norm: ", gradient_norm, "function value: ", f(initial_position))
            alfa_i /= 2

            if(alfa_i < 1e-15):
                if(verbose): print("steepest descent reached a local minimum (alfa): " , initial_position)
                return initial_position
        
        iteration_counter += 1

    if(verbose): print("steepest descent reached a local minimum (iteration): ", initial_position)
    return initial_position



