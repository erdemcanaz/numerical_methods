def mullers_method(f = None, x_0 = None, x_1 = None, x_2 = None, ABSOLUTE_Y_ERROR = 1e-15,  MAX_ITERATION =  60, verbose = True):
    if f == None:
        raise ValueError("f is not defined.")
    elif x_0 == None or x_1 == None or x_2 == None:
        raise ValueError("Initial points are not given.")
    elif f(x=x_0) == 0:
        return x_0
    elif f(x=x_1) == 0:
        return x_1
    elif f(x=x_2) == 0:
        return x_2
    elif x_0 == x_1 or x_0 == x_2 or x_1 == x_2:
        raise ValueError("Initial points can not be the same.")

    if(verbose):print(f"\nApplying Muller's method to f(x)={f.__name__} with initial points x= ({x_0} , {x_1} , {x_2})")

    def second_order_lagrange_polynomial_roots(f = None, x_0 = 0, x_1 = 0, x_2 = 0):
        if(x_0 == x_1 or x_0 == x_2 or x_1 == x_2):
            raise ValueError("lagrange polynomial: Initial points can not be the same .")

        alfa_0 = f(x=x_0)/((x_0-x_1)*(x_0-x_2))
        alfa_1 = f(x=x_1)/((x_1-x_0)*(x_1-x_2))
        alfa_2 = f(x=x_2)/((x_2-x_0)*(x_2-x_1))

        #for ax^2 + bx + c
        a = alfa_0 + alfa_1 + alfa_2
        b = -(alfa_0*(x_1+x_2) + alfa_1*(x_0+x_2) + alfa_2*(x_0+x_1))
        c = alfa_0*x_1*x_2 + alfa_1*x_0*x_2 + alfa_2*x_0*x_1

        root_1 = (-b + (b**2 - 4*a*c)**0.5)/(2*a)
        root_2 = (-b - (b**2 - 4*a*c)**0.5)/(2*a)

        return root_1, root_2

    
    iteration_counter = 0
    while iteration_counter < MAX_ITERATION:

        root_1,root_2 = second_order_lagrange_polynomial_roots(f=f, x_0=x_0, x_1=x_1, x_2=x_2)
        x_0 = x_1
        x_1 = x_2
        x_2 = root_1 if abs(x_2-root_1) < abs(x_2-root_2) else root_2

        if(abs(f(x=x_2)) < ABSOLUTE_Y_ERROR):
            if(verbose):print(f"Absolute y error: {abs(f(x=x_2))}")
            return x_2
        elif iteration_counter >= (MAX_ITERATION-1):
            if(verbose):print(f"Max iteration: {iteration_counter+1}")
            return x_2
        
        print(f"Iteration: {iteration_counter+1} , x_0={x_0}, x_1={x_1}, x_2={x_2}, f(x_2)={f(x=x_2)}" )
        iteration_counter += 1

def newton_raphson_method(f = None, f_prime = None, x_0 = None, ABSOLUTE_Y_ERROR = 1e-15, MAX_ITERATION =  100, verbose = True):
    #Absolute y error: if f(x) is smaller than this value, then return x
    #Max iteration: if iteration count is larger than this value, then return x. Note that 2^50 > 1.1258999e+15.

    if f == None:
        raise ValueError("f is not defined.")
    elif f_prime == None:
        raise ValueError("f_prime is not defined.")
    elif x_0 == None:
        raise ValueError("Initial point is not given.")
    elif f(x=x_0) == 0:
        return x_0
    
    if(verbose):print(f"\nApplying Newton-Raphson method to f(x)={f.__name__} with initial point x={x_0}")
    iteration_counter = 0
    while iteration_counter < MAX_ITERATION:
        if(f_prime(x=x_0) == 0):
            raise ValueError("f_prime(x) is zero.")
        x_0 = x_0 - f(x=x_0)/f_prime(x=x_0)
        if(abs(f(x=x_0)) < ABSOLUTE_Y_ERROR):
            if(verbose):print(f"Absolute y error: {abs(f(x=x_0))}")
            return x_0
        elif iteration_counter >= (MAX_ITERATION-1):
            if(verbose):print(f"Max iteration: {iteration_counter+1}")
            return x_0
        if(verbose):print(f"Iteration: {iteration_counter+1} , x={x_0}, f(x)={f(x=x_0)}" )   
        iteration_counter += 1

def secant_method(f = None, x_0 = None, x_1 = None, ABSOLUTE_Y_ERROR = 1e-15,  MAX_ITERATION =  100, verbose = True):
    #Absolute y error: if f(x) is smaller than this value, then return x
    #Max iteration: if iteration count is larger than this value, then return x. Note that 2^50 > 1.1258999e+15.   

    if f == None:
      raise ValueError("f is not defined.")
    elif x_0 == None or x_1 == None:
      raise ValueError("Initial points are not given.")
    elif f(x=x_0) == 0:
      return x_0
    elif f(x=x_1) == 0:
        return x_1
    elif x_0 == x_1:
        raise ValueError("Initial points can not be the same.")


    if(verbose):print(f"\nApplying secant method to f(x)={f.__name__} with initial point x= ({x_0} , {x_1})")
    iteration_counter = 0
    while iteration_counter < MAX_ITERATION:
        m=(f(x=x_1)-f(x=x_0))/(x_1-x_0)
        if m == 0:
           raise ValueError("Slope is zero.")
        x_0 = x_1
        x_1 = x_1 - f(x=x_1)/m
        if(abs(f(x=x_1)) < ABSOLUTE_Y_ERROR):
            if(verbose):print(f"Absolute y error: {abs(f(x=x_1))}")
            return x_1
        elif iteration_counter >= (MAX_ITERATION-1):
            if(verbose):print(f"Max iteration: {iteration_counter+1}")
            return x_1
        if(verbose):print(f"Iteration: {iteration_counter+1} , x_0={x_0}, x_1={x_1} f(x_1)={f(x=x_1)}" )   
        iteration_counter += 1

def false_position_method(f = None, left_x = None, right_x = None, ABSOLUTE_Y_ERROR = 1e-15,  ABSOLUTE_X_ERROR = 1e-15, RELATIVE_X_ERROR =  1e-15, MAX_ITERATION =  100, verbose = True):
    #Absolute y error: if f(x) is smaller than this value, then return x
    #Absolute x error: if approximated x is closer to exact value smaller than this value, then return x
    #Relative x error: if (bracket length)/(x_left) smaller than this value, then return x
    #Max iteration: if iteration count is larger than this value, then return x. Note that 2^50 > 1.1258999e+15.   
                      
    if f == None:
      raise ValueError("f is not defined.")
    elif left_x == None or right_x == None:
      raise ValueError("Initial brackets are not given.")
    elif left_x >= right_x:
        raise ValueError("Left bracket is not smaller than right bracket.")
    elif f(x=left_x) == 0:
      return left_x
    elif f(x=right_x) == 0:
        return right_x
    elif f(x=left_x) * f(x=right_x) > 0:
        raise ValueError("Initial brackets do not guaranteed to have a solution by IVT.")    
    
    if(verbose):print(f"\nApplying false-position method to f(x)={f.__name__} with initial brackets ({left_x},{right_x})")
    iteration_counter = 0
    while True:        

        #update brackets
        m = (f(x=right_x) - f(x=left_x))/(right_x - left_x)
        del_x = -f(x=left_x)/m
        x_next = left_x + del_x
        y_next = f(x=x_next)


        if(abs(y_next) < ABSOLUTE_Y_ERROR):#Absolute y error:
            if(verbose):print(f"Absolute y error: {abs(y_next)}")
            return x_next
        elif f(x=left_x) * f(x=x_next) < 0:
            right_x = x_next
        else:
            left_x = x_next

        #check convergence
        if (right_x - left_x < ABSOLUTE_X_ERROR): #Absolute x error:
            if(verbose):print(f"Absolute x error: {right_x - left_x}")
            return x_next
        elif( (right_x - left_x)/(min(abs(left_x),abs(right_x))+1e-10) < RELATIVE_X_ERROR ): #Relative x error
            if(verbose):print(f"Relative x error: {(right_x - left_x)/(min(abs(left_x),abs(right_x)))}")
            return x_next
        elif iteration_counter >= (MAX_ITERATION-1): #Max iteration
            if(verbose):print(f"Max iteration: {iteration_counter+1}")
            return x_next
        
        if(verbose):print(f"Iteration: {iteration_counter+1} , ({left_x} , {right_x}), y={f(x=(left_x + right_x)/2)}" )
        iteration_counter += 1

def bisection_method(f = None, left_x = None, right_x = None, ABSOLUTE_Y_ERROR = 1e-15,  ABSOLUTE_X_ERROR = 1e-15, RELATIVE_X_ERROR =  1e-15, MAX_ITERATION =  75, verbose = True):
    #Absolute y error: if f(x) is smaller than this value, then return x
    #Absolute x error: if approximated x is closer to exact value smaller than this value, then return x
    #Relative x error: if (bracket length)/(x_left) smaller than this value, then return x
    #Max iteration: if iteration count is larger than this value, then return x. Note that 2^50 > 1.1258999e+15. 
    
    if f == None:
      raise ValueError("f is not defined.")
    elif left_x == None or right_x == None:
      raise ValueError("Initial brackets are not given.")
    elif left_x >= right_x:
        raise ValueError("Left bracket is not smaller than right bracket.")
    elif f(x=left_x) == 0:
      return left_x
    elif f(x=right_x) == 0:
        return right_x
    elif f(x=left_x) * f(x=right_x) > 0:
        raise ValueError("Initial brackets do not guaranteed to have a solution by IVT.")    
    
    if(verbose):print(f"\nApplying bisection method to f(x)={f.__name__} with initial brackets ({left_x},{right_x})")
    iteration_counter = 0
    while iteration_counter < MAX_ITERATION:

        #update brackets
        x_mid = (left_x + right_x)/2
        y_mid = f(x=x_mid)
        if(abs(y_mid) < ABSOLUTE_Y_ERROR):#Absolute y error:
            if(verbose):print(f"Absolute y error: {abs(y_mid)}")
            return x_mid 
        elif f(x=left_x) * f(x=x_mid) < 0:
            right_x = x_mid
        else:
            left_x = x_mid

        #check convergence
        if (right_x - left_x < ABSOLUTE_X_ERROR): #Absolute x error: 
            if(verbose):print(f"Absolute x error: {right_x - left_x}")
            return x_mid
        elif( (right_x - left_x)/(min(abs(left_x),abs(right_x))+1e-15) < RELATIVE_X_ERROR): #Relative x error
            if(verbose):print(f"Relative x error: {(right_x - left_x)/(min(abs(left_x),abs(right_x)))}")
            return x_mid
        elif iteration_counter >= (MAX_ITERATION-1): #Max iteration
            if(verbose):print(f"Max iteration: {iteration_counter+1}")
            return x_mid        

        if(verbose):print(f"Iteration: {iteration_counter+1} , ({left_x} , {right_x}), f={f(x=(left_x + right_x)/2)}" )
        iteration_counter += 1

        
        

   
    