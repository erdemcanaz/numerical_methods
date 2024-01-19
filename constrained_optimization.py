import numpy as np
import matplotlib.pyplot as plt

x1 = lambda t: (1-t**2)/t
x2 = lambda t: t
f = lambda x1,x2: x1+2*x2

t_samples_pos = np.linspace(0.5, 1.5 , 100)
t_samples_neg = np.linspace(-1.5, -0.5 , 100)

x_samples = []
y_samples = []
for t in t_samples_neg:
    x_samples.append(t)
    y_samples.append(f(x1(t),x2(t)))

   

plt.plot(x_samples, y_samples)
plt.xlabel('x')
plt.ylabel('y')
plt.title('Plot of x and y')
plt.show()
