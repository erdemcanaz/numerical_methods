def false_position_method(f = None, left_x = None, right_x = None, ABSOLUTE_Y_ERROR = 1e-15,  ABSOLUTE_X_ERROR = 1e-15, RELATIVE_X_ERROR =  1e-15, MAX_ITERATION =  55, verbose = True):
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

def bisection_method(f = None, left_x = None, right_x = None, ABSOLUTE_Y_ERROR = 1e-15,  ABSOLUTE_X_ERROR = 1e-15, RELATIVE_X_ERROR =  1e-15, MAX_ITERATION =  55, verbose = True):
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
        elif( (right_x - left_x)/(min(abs(left_x),abs(right_x))) < RELATIVE_X_ERROR+1e-10): #Relative x error
            if(verbose):print(f"Relative x error: {(right_x - left_x)/(min(abs(left_x),abs(right_x)))}")
            return x_mid
        elif iteration_counter >= (MAX_ITERATION-1): #Max iteration
            if(verbose):print(f"Max iteration: {iteration_counter+1}")
            return x_mid        

        if(verbose):print(f"Iteration: {iteration_counter+1} , ({left_x} , {right_x}), f={f(x=(left_x + right_x)/2)}" )
        iteration_counter += 1

        
        

   
    