import sympy as sp

# Define the symbols for vector x, treating some indices as numbers


x1, x2, x3 = sp.symbols('x1 x2 x3')

# Define the symbols for matrix Q, treating some indices as numbers
a11, a12, a13 = 3, -1, -1  # treating a11 as a number
a21, a22, a23 = -1, 2, 0  # treating a22 as a number
a31, a32, a33 = -1, 0, 1  # treating a33 as a number


x_T = sp.Matrix([[x1, x2, x3]])
x = sp.Matrix([[x1], [x2], [x3]])
Q = sp.Matrix([[a11, a12, a13],
               [a21, a22, a23],
               [a31, a32, a33]])

# Perform the multiplication x^T * Q * x
result = (0.5)* x_T * Q * x
sp.pprint(result)

# Simplify the resulting expression
simplified_result = sp.simplify(result[0])
expanded_simplified_result = sp.expand(simplified_result)
final_simplified_result = sp.simplify(expanded_simplified_result)

# Print the simplified result
print(final_simplified_result)
