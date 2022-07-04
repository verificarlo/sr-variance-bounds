#!/usr/bin/python3

import sys
import re
import numpy as np

import matplotlib
from fractions import Fraction
from numpy.lib.type_check import real
# Use Agg backend for headless runs
matplotlib.use('Agg')

import matplotlib.pyplot as plt
import math

# SR unit-roundoff
u = 2**(-23)

# lambda
lam = 0.5

# Define plot title and labels
plt.title("$1-\lambda$ = {} ".format(1-lam))
plt.xlabel("$N$")
plt.xlim(7.5,26.5)
plt.xticks(range(8,27,2))

# bounds
det_bound = []
azuma = []
cheby = []

# numerator 
num = int(sys.argv[1])

# denominator 
deno = int(sys.argv[2])

# x value
x = Fraction(num,deno)

# vector of polynomial degree
array_n = []

# polynomial degree
k = 8

# gamma
gamma2 = (1+u)**(2*k) -1 
gamma4 = (1+u)**(4*k) -1 
gamma = (1+u**2)**(2*k) -1

# max polynomial degree
max = int(sys.argv[3])

while k < (max + 1):
    # coef
    a = []

    # read all coef from file
    f = open('result'+ str(k) +'.txt', 'r')
    for line in f:
        a.append(float(line))

    # read exact value p(x)
    f = open('resultt'+ str(k) +sys.argv[1]+'.txt', 'r')
    for line in f:
        Txx = float(Fraction(line)) 

    # absp = sum of the absolute value of coefficients and x
    absp = abs(a[0]) 
    for i in range(1,len(a)):
         absp  =  absp  + abs(a[i]*(x**(2*i)))
    
    # read all results from file
    dtype3 = np.dtype([('res', np.float32)]) 
    D = np.loadtxt('global_'+ str(k) +'.tsv', skiprows=0, dtype = dtype3)
    
    # 30 times the x value
    array_k = []

    # SR errors
    sr = [] 

    # forward error/cond(P)
    for i in range(30):
        array_k.append(k)
        sr.append( np.abs((D['res'][i] -Txx)/absp) )

    # plot SR points
    if k== deno:
        plt.plot(array_k, sr, ' +', color='r', label = 'SR-nearness/cond(P,x)')
    plt.plot(array_k, sr, ' +', color='r')
   
    det_bound.append( gamma2 )
    azuma.append( math.sqrt(u*gamma4*math.log(2.0/lam)))
    cheby.append( math.sqrt(gamma*(1.0/lam)))  
    array_n.append(k)

    k=k+2
    gamma2 = (1+u)**(2*k) -1 
    gamma4 = (1+u)**(4*k) -1 
    gamma = (1+u**2)**(2*k) -1

# Plot the deterministic and probabilistic upper bounds on forward error    
plt.plot(array_n, det_bound,  linestyle=':', color='b', label = "(deterministic bound)/cond(P,x)")
plt.plot(array_n, azuma, '--', color='g', label = "(AH bound)/cond(P,x)")
plt.plot(array_n, cheby, color='c', label = "(BC bound)/cond(P,x)")


ax = plt.gca()

def sci_format(x,lim):
    return '{:.1e}'.format(x)
from matplotlib.ticker import FuncFormatter
ax.get_yaxis().set_major_formatter(FuncFormatter(sci_format))
plt.ylabel("$Error/cond(P,x)$")
plt.gcf().subplots_adjust(bottom=0.15)
plt.tight_layout()



plt.show()
plt.legend()

plotname = "horner-plot" +sys.argv[1]+"-" + sys.argv[2] +".pdf"
plt.savefig(plotname, format='pdf')    
