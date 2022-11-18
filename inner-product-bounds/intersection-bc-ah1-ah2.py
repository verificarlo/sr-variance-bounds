import math
import matplotlib.pyplot as plt
from mpmath import *
import numpy as np

mp.dps=50

# SR unit-roundoff
u = mpf(2**(-23))

# Lambda
lam = mpf(1 - 0.9)

# Bounds
ah1 = []
ah2 = []
bc = []

# x-coordinate
x = []

# Lower and upper n values
mi = 10**5
ma = 10**8

# Compute the bounds across increasing n
for nn in range(mi, ma, ma//1000):
    n = mpf(nn)
    z = math.log(2*n / lam)
    ah1.append( math.exp( (u * math.sqrt(2*n*z) +  n*u**2 )/ (1.0- u)) -1 )

    ah2.append(mp.sqrt(u*((mpf(1)+u)**(mpf(2)*n)-mpf(1))
        * mp.log(mpf(2)/lam)) )
   

    bc.append(mp.sqrt(((mpf(1)+u**mpf(2))**(n)-mpf(1))
        *mpf(1)/lam) )
    x.append( n )

# Define plot title and labels
plt.title("$1-\lambda = 0.9$")
plt.xlabel("$n$")
plt.yscale('log')
plt.xscale('log')

# Plot the upper bounds of the forward error
plt.plot(x, ah1, linestyle = 'dashdot', color='m', label = "AH1 bound" )
plt.plot(x, ah2, linestyle = '--', color='g', label = "AH2 bound" )
plt.plot(x, bc, color='c', label = "BC bound")

# Intersections points
delta = np.array([yy1-yy2 for yy1,yy2 in zip(ah1,ah2)])
idx = np.argwhere(np.diff(np.sign(delta))).flatten()[0]
plt.plot(x[idx], ah1[idx], 'ro')
theta = np.array([yy1-yy2 for yy1,yy2 in zip(ah2,bc)])
idx = np.argwhere(np.diff(np.sign(theta))).flatten()[0]
plt.plot(x[idx], ah2[idx], 'ro')
print("intersection = %g"%float(x[idx]))


plt.legend()
plt.show()

plotname = "intersection-bc-ah1-ah2.pdf"
plt.savefig(plotname, format='pdf')  
