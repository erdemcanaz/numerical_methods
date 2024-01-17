import math

def dichotomous_search(f = None, interval = None , desired_interval_length = 1e-6, EPS = 1e-9, ITMAX = 75, verbose = True) -> float:
    # f is the function to be minimized
    # interval is a list of two numbers, the left and right endpoints of the interval
    # desired_interval_length is the length of the interval that we want to achieve
    # EPS is the absolute error tolerance
    # ITMAX is the maximum number of iterations
    # verbose is a boolean that determines whether or not to print the iterations

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

        
    



