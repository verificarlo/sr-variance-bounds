import math
import matplotlib.pyplot as plt
import numpy as np

# SR unit-roundoff
u = 2**(-23)

# Lambda
lam = 0.1

# Bounds
ah1 = []
bc = []

# x-coordinate 
x = []

# Lower and upper n values
mi = 10**10
ma = 10**15

# Compute the bounds across increasing n
for n in range(mi, ma, ma//1000):
    z = math.sqrt(2*n*math.log(2*n / lam) )
    ah1.append( math.exp( (u*z  +  n*u**2 )/ (1.0- u)) -1 )
    x.append( n )
    bc.append( math.sqrt( ( (1+(u)**2)**(n)-1)*(1.0/(lam)) ) )

# Plot the upper bounds of the forward error
plt.plot(x, ah1, linestyle = 'dashdot', color='m', label = 'AH1 bound')
plt.plot(x, bc, color='c', label = 'BC bound') 

# Define plot title and labels
title = "1 - $\lambda$ = {} ".format(1-lam)
plt.suptitle(title)
plt.xlabel("$n$")
plt.yscale('log')
plt.xscale('log')

plt.legend()
plt.savefig("bc_vs_ah1.pdf", format='pdf')
plt.show()
