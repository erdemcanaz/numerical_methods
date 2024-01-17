

def dichotomous_search(f = None, interval = None , desired_interval_length = 1e-6, EPS = 1e-9, ITMAX = 75, verbose = True):
    # f is the function to be minimized
    # interval is a list of two numbers, the left and right endpoints of the interval
    # EPS is the absolute error tolerance

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

        
         



        
    



